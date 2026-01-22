from fastapi import FastAPI, status, text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from .config import get_settings
from .database import engine, Base, SessionLocal
from .models.user import User
from .services.auth_service import hash_password
from .routes import auth, os as os_routes, relatorios, usuarios

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa o banco de dados e cria usuários padrão
    Base.metadata.create_all(bind=engine)
    
    # Atualiza o schema (Migrações manuais simples)
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS motivo_abertura VARCHAR;"))
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS telegram_nick VARCHAR;"))
            conn.execute(text("ALTER TABLE ordens_servico ADD COLUMN IF NOT EXISTS telegram_phone VARCHAR;"))
            print("✅ Schema atualizado com sucesso!")
        except Exception as e:
            print(f"⚠️ Aviso ao atualizar schema: {e}")
    db = SessionLocal()
    try:
        # Verifica se já existem usuários
        if db.query(User).count() == 0:
            print("🆕 Criando usuários padrão...")
            users = [
                User(username="admin", password_hash=hash_password("admin123"), role="admin"),
                User(username="monitor", password_hash=hash_password("monitor123"), role="monitor"),
                User(username="tecnico1", password_hash=hash_password("tecnico123"), role="execucao")
            ]
            db.add_all(users)
            db.commit()
            print("✅ Usuários padrão criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
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

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(os_routes.router, prefix="/api/v1")
app.include_router(relatorios.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")

# Serve Static Files (Frontend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")


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
