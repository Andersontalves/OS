"""
Script to initialize the database with sample users

Run this after setting up the database:
    python init_db.py
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.services.auth_service import hash_password


def init_database():
    """Initialize database with sample users"""
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas!")
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  Banco já contém {existing_users} usuários. Pulando inicialização.")
            return
        
        print("\n📝 Criando usuários padrão...")
        
        # Create sample users
        users = [
            User(
                username="admin",
                password_hash=hash_password("admin123"),
                role="admin",
                nome="Administrador do Sistema"
            ),
            User(
                username="monitor",
                password_hash=hash_password("monitor123"),
                role="monitoramento",
                nome="Monitor de Operações"
            ),
            User(
                username="tecnico1",
                password_hash=hash_password("tecnico123"),
                role="execucao",
                nome="Técnico Executor 1"
            ),
            User(
                username="tecnico2",
                password_hash=hash_password("tecnico123"),
                role="execucao",
                nome="Técnico Executor 2"
            ),
            User(
                username="campo1",
                password_hash=hash_password("campo123"),
                role="campo",
                nome="Técnico de Campo 1",
                telegram_id=None  # Will be set when bot registers
            ),
        ]
        
        db.add_all(users)
        db.commit()
        
        print("✅ Usuários criados com sucesso!\n")
        print("=" * 60)
        print("CREDENCIAIS DE ACESSO:")
        print("=" * 60)
        print("\n👤 ADMIN (Acesso total)")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👁️  MONITORAMENTO (Somente leitura)")
        print("   Username: monitor")
        print("   Password: monitor123")
        print("\n🔧 EXECUÇÃO (Assumir e finalizar O.S)")
        print("   Username: tecnico1")
        print("   Password: tecnico123")
        print("\n🔧 EXECUÇÃO (Assumir e finalizar O.S)")
        print("   Username: tecnico2")
        print("   Password: tecnico123")
        print("\n📱 CAMPO (Telegram - não usa painel web)")
        print("   Username: campo1")
        print("   Password: campo123")
        print("\n" + "=" * 60)
        print("⚠️  ATENÇÃO: Altere essas senhas em produção!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
