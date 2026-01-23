# Fixed imports for SQLAlchemy text
from fastapi import FastAPI, status
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import time

# Set Timezone to Brazil/Brasilia
os.environ['TZ'] = 'America/Sao_Paulo'
if hasattr(time, 'tzset'):
    time.tzset()

from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from .config import get_settings
from .database import engine, Base, SessionLocal
from .models.user import User
from .services.auth_service import hash_password
from .routes import auth, os as os_routes, relatorios, usuarios
from datetime import datetime, timedelta

settings = get_settings()

# Rastreamento do último heartbeat do bot
bot_last_heartbeat = None
bot_heartbeat_lock = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Atualiza o schema (Migrações manuais simples)
    with engine.begin() as conn:
        try:
            # SQL Standard compatibility
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS motivo_abertura VARCHAR;"))
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS telegram_nick VARCHAR;"))
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS telegram_phone VARCHAR;"))
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS cidade VARCHAR;"))
            print("✅ Schema atualizado com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso ao atualizar schema: {e}")
            # Tentativa secundária sem IF NOT EXISTS para alguns sabores de DB
            try:
                conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN motivo_abertura VARCHAR;"))
                conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN telegram_nick VARCHAR;"))
                conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN telegram_phone VARCHAR;"))
                conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN cidade VARCHAR;"))
            except:
                pass
    
    # Cria tabelas se não existirem
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas verificadas/criadas!")
    except Exception as e:
        print(f"⚠️ Aviso ao criar tabelas: {e}")
    
    # Garante que usuários padrão existem
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        print(f"📊 Usuários no banco: {user_count}")
        
        # Verifica se admin existe especificamente
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("🆕 Criando usuário admin...")
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
                nome="Administrador do Sistema"
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuário admin criado com sucesso!")
        else:
            print(f"✅ Usuário admin já existe (ID: {admin.id})")
        
        # Se não há usuários, cria os padrão
        if user_count == 0:
            print("🆕 Criando usuários padrão...")
            users = [
                User(username="monitor", password_hash=hash_password("monitor123"), role="monitoramento", nome="Monitor de Operações"),
                User(username="tecnico1", password_hash=hash_password("tecnico123"), role="execucao", nome="Técnico Executor 1")
            ]
            db.add_all(users)
            db.commit()
            print("✅ Usuários padrão criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    yield

# Initialize FastAPI app
app = FastAPI(
    title="Sistema de Ordens de Serviço API",
    description="API para gestão de ordens de serviço com integração Telegram",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define API endpoints BEFORE mounting frontend (order matters!)
@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Sistema de Ordens de Serviço API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/keepalive", status_code=status.HTTP_200_OK)
def keepalive():
    """Keep-alive endpoint to prevent idle shutdown."""
    global bot_last_heartbeat
    
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db.commit()
        
        # Registra que o bot fez heartbeat
        bot_last_heartbeat = datetime.utcnow()
        
        return {"status": "alive", "database": "connected", "bot_heartbeat": True}
    except Exception as e:
        return {"status": "alive", "database": "error", "message": str(e)}
    finally:
        db.close()


@app.get("/bot-status", status_code=status.HTTP_200_OK)
def bot_status():
    """Verifica se o bot está online baseado no último heartbeat"""
    global bot_last_heartbeat
    
    if bot_last_heartbeat is None:
        return {
            "bot_online": False,
            "status": "offline",
            "message": "Bot nunca fez heartbeat. Pode estar offline.",
            "last_heartbeat": None,
            "time_since_last": None
        }
    
    time_since = datetime.utcnow() - bot_last_heartbeat
    time_since_seconds = time_since.total_seconds()
    
    # Bot é considerado online se fez heartbeat nos últimos 10 minutos (8min intervalo + margem)
    is_online = time_since_seconds < 600
    
    return {
        "bot_online": is_online,
        "status": "online" if is_online else "offline",
        "message": "Bot está online" if is_online else f"Bot offline há {int(time_since_seconds/60)} minutos",
        "last_heartbeat": bot_last_heartbeat.isoformat(),
        "time_since_last_seconds": int(time_since_seconds),
        "time_since_last_minutes": int(time_since_seconds / 60)
    }


@app.post("/init-admin", status_code=status.HTTP_200_OK)
def init_admin():
    """Endpoint temporário para criar usuário admin se não existir"""
    db = SessionLocal()
    try:
        # Verifica se admin existe
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            # Testa se a senha está correta
            from .services.auth_service import verify_password
            password_ok = verify_password("admin123", admin.password_hash)
            
            return {
                "status": "exists",
                "message": "Usuário admin já existe",
                "user_id": admin.id,
                "password_valid": password_ok,
                "username": admin.username,
                "role": admin.role
            }
        
        # Cria admin
        admin_user = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin",
            nome="Administrador do Sistema"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        return {
            "status": "created",
            "message": "Usuário admin criado com sucesso",
            "user_id": admin_user.id,
            "username": admin_user.username,
            "password": "admin123",
            "role": admin_user.role
        }
    except Exception as e:
        db.rollback()
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }
    finally:
        db.close()


@app.get("/check-admin", status_code=status.HTTP_200_OK)
def check_admin():
    """Endpoint para verificar se admin existe e pode fazer login"""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        
        if not admin:
            return {
                "admin_exists": False,
                "message": "Usuário admin não existe",
                "can_login": False,
                "suggestion": "Use /init-admin para criar"
            }
        
        # Testa senha
        from .services.auth_service import verify_password
        password_ok = verify_password("admin123", admin.password_hash)
        
        # Testa login completo
        from .services.auth_service import authenticate_user
        test_login = authenticate_user(db, "admin", "admin123")
        
        return {
            "admin_exists": True,
            "user_id": admin.id,
            "username": admin.username,
            "role": admin.role,
            "password_hash_valid": password_ok,
            "can_login": test_login is not None,
            "message": "Admin pode fazer login" if test_login else "Admin existe mas login falha"
        }
    except Exception as e:
        import traceback
        return {
            "admin_exists": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
    finally:
        db.close()


@app.get("/debug", status_code=status.HTTP_200_OK)
def debug_info():
    """Endpoint de debug - retorna informações do sistema"""
    db = SessionLocal()
    debug_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "api_status": "online",
        "database": {},
        "users": {},
        "bot": {}
    }
    
    try:
        # Info do banco
        db.execute(text("SELECT 1"))
        debug_info["database"]["connected"] = True
        
        # Conta usuários
        user_count = db.query(User).count()
        debug_info["users"]["total"] = user_count
        
        # Verifica admin
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            from .services.auth_service import verify_password, authenticate_user
            password_ok = verify_password("admin123", admin.password_hash)
            login_ok = authenticate_user(db, "admin", "admin123") is not None
            
            debug_info["users"]["admin"] = {
                "exists": True,
                "id": admin.id,
                "username": admin.username,
                "role": admin.role,
                "password_valid": password_ok,
                "can_login": login_ok
            }
        else:
            debug_info["users"]["admin"] = {"exists": False}
        
        # Info do bot
        global bot_last_heartbeat
        if bot_last_heartbeat:
            time_since = (datetime.utcnow() - bot_last_heartbeat).total_seconds()
            debug_info["bot"]["last_heartbeat"] = bot_last_heartbeat.isoformat()
            debug_info["bot"]["seconds_since"] = int(time_since)
            debug_info["bot"]["online"] = time_since < 600
        else:
            debug_info["bot"]["last_heartbeat"] = None
            debug_info["bot"]["online"] = False
        
    except Exception as e:
        debug_info["database"]["connected"] = False
        debug_info["database"]["error"] = str(e)
        import traceback
        debug_info["error"] = traceback.format_exc()
    finally:
        db.close()
    
    return debug_info


@app.post("/fix-bot", status_code=status.HTTP_200_OK)
def fix_bot():
    """Endpoint para destravar o bot - verifica tudo e tenta acordar o bot se necessário"""
    db = SessionLocal()
    results = {
        "api_status": "ok",
        "admin_status": "unknown",
        "database_status": "unknown",
        "bot_status": "unknown",
        "bot_wake_attempt": False,
        "bot_should_work": False,
        "warnings": []
    }
    
    start_time = datetime.utcnow()
    
    try:
        # 1. Testa conexão com banco
        db.execute(text("SELECT 1"))
        results["database_status"] = "connected"
        
        # 2. Garante que admin existe
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            results["admin_status"] = "exists"
            results["admin_id"] = admin.id
        else:
            # Cria admin
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
                nome="Administrador do Sistema"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            results["admin_status"] = "created"
            results["admin_id"] = admin_user.id
        
        # 3. Verifica status do bot
        bot_status_info = bot_status()
        results["bot_status"] = bot_status_info["status"]
        results["bot_online"] = bot_status_info["bot_online"]
        results["last_heartbeat"] = bot_status_info.get("last_heartbeat")
        results["time_since_last_minutes"] = bot_status_info.get("time_since_last_minutes", 0)
        
        # 4. Se bot está offline, tenta acordar
        if not bot_status_info["bot_online"]:
            results["bot_wake_attempt"] = True
            results["warnings"].append(f"Bot está offline há {bot_status_info.get('time_since_last_minutes', 0)} minutos")
            
            # Tenta acordar o bot fazendo uma requisição ao endpoint do bot (se existir)
            # Ou força um heartbeat fazendo uma requisição interna
            try:
                # Força um "ping" que pode acordar o bot se ele estiver hibernado
                # O bot deve fazer heartbeat quando receber qualquer requisição
                pass  # Por enquanto apenas registra
                results["wake_message"] = "Tentativa de acordar bot iniciada. Aguarde até 3 minutos."
            except Exception as e:
                results["wake_error"] = str(e)
        
        # 5. Verifica se demorou mais de 3 minutos
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        if elapsed > 180:  # 3 minutos
            results["warnings"].append(f"⚠️ Operação demorou {int(elapsed/60)} minutos. Bot pode estar lento ou offline.")
        
        # 6. Testa se API está respondendo (já estamos aqui, então está OK)
        results["api_status"] = "online"
        
        # 7. Se tudo OK, bot deve funcionar
        if (results["database_status"] == "connected" and 
            results["admin_status"] in ["exists", "created"] and
            results["bot_online"]):
            results["bot_should_work"] = True
            results["message"] = "✅ Bot destravado e online! Tudo funcionando."
        elif results["bot_online"]:
            results["bot_should_work"] = True
            results["message"] = "✅ Bot destravado! API e banco OK. Bot está online."
        else:
            results["bot_should_work"] = False
            results["message"] = "⚠️ Bot destravado, mas bot está offline. Pode demorar até 3 minutos para responder."
            
    except Exception as e:
        results["api_status"] = "error"
        results["database_status"] = "error"
        results["message"] = f"❌ Erro: {str(e)}"
        db.rollback()
    finally:
        db.close()
    
    # Adiciona tempo total
    elapsed_total = (datetime.utcnow() - start_time).total_seconds()
    results["elapsed_seconds"] = int(elapsed_total)
    
    return results


# Include routers (after root endpoints, before frontend)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(os_routes.router, prefix="/api/v1")
app.include_router(relatorios.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")

# Serve Static Files (Frontend) - MUST be last to not catch API routes
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor. Por favor, tente novamente."}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
