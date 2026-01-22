"""
Script para testar conexão com o banco de dados
Útil para verificar se a migração para Supabase funcionou
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

sys.path.append(str(Path(__file__).parent))

from app.database import engine, SessionLocal
from app.models.user import User
from app.models.ordem_servico import OrdemServico
from sqlalchemy import text

def test_connection():
    """Testa conexão com o banco"""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./os_database.db")
    
    print("🔍 Testando conexão com banco de dados...")
    print(f"   URL: {database_url[:50]}..." if len(database_url) > 50 else f"   URL: {database_url}")
    
    try:
        # Testa conexão básica
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão estabelecida!")
            
            # Detecta tipo de banco
            if "postgresql" in database_url.lower():
                db_version = conn.execute(text("SELECT version()")).scalar()
                print(f"   Tipo: PostgreSQL")
                print(f"   Versão: {db_version[:50]}...")
            elif "sqlite" in database_url.lower():
                print(f"   Tipo: SQLite")
            else:
                print(f"   Tipo: Desconhecido")
        
        # Testa tabelas
        print("\n📊 Verificando tabelas...")
        with SessionLocal() as db:
            user_count = db.query(User).count()
            ordem_count = db.query(OrdemServico).count()
            
            print(f"   ✅ Tabela 'users': {user_count} registros")
            print(f"   ✅ Tabela 'ordens_servico': {ordem_count} registros")
            
            if user_count > 0:
                print("\n👥 Usuários encontrados:")
                users = db.query(User).limit(5).all()
                for user in users:
                    print(f"   - {user.username} ({user.role})")
        
        print("\n✅ Teste concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao conectar: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
