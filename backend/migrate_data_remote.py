"""
Script para migrar dados do backup para Supabase
Pode ser executado diretamente no servidor (Render/Railway)
"""
import os
import json
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

def migrate_users_from_backup(backup_file: str = "backup_sqlite_20260122_194850.json"):
    """Migra usuários do backup para o Supabase"""
    
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("ERRO: DATABASE_URL nao configurado!")
        return False
    
    # Tenta carregar o backup (pode não existir no servidor)
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de backup {backup_file} nao encontrado.")
        print("Criando usuario admin padrao...")
        return create_default_admin(database_url)
    
    print("Conectando ao Supabase...")
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        try:
            # Verifica se já existem usuários
            result = session.execute(text("SELECT COUNT(*) FROM users")).scalar()
            if result > 0:
                print(f"AVISO: Ja existem {result} usuarios no banco. Pulando migracao.")
                return True
            
            # Migra usuários do backup
            print("Migrando usuarios do backup...")
            users = backup_data["tables"].get("users", [])
            
            for user_data in users:
                user_insert = user_data.copy()
                user_id = user_insert.pop('id', None)
                session.execute(
                    text("""
                        INSERT INTO users (username, password_hash, role, telegram_id, nome, created_at)
                        VALUES (:username, :password_hash, :role, :telegram_id, :nome, :created_at)
                        ON CONFLICT (username) DO NOTHING
                    """),
                    user_insert
                )
            
            session.commit()
            print(f"OK: {len(users)} usuarios migrados com sucesso!")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"ERRO na migracao: {e}")
            import traceback
            traceback.print_exc()
            return False

def create_default_admin(database_url: str):
    """Cria usuário admin padrão se não existir"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    
    # Hash da senha "admin123"
    password_hash = pwd_context.hash("admin123")
    
    engine = create_engine(database_url)
    with Session(engine) as session:
        try:
            # Verifica se admin já existe
            result = session.execute(
                text("SELECT id FROM users WHERE username = 'admin'")
            ).first()
            
            if result:
                print("OK: Usuario admin ja existe.")
                return True
            
            # Cria admin
            session.execute(
                text("""
                    INSERT INTO users (username, password_hash, role, nome, created_at)
                    VALUES ('admin', :password_hash, 'admin', 'Admin', NOW())
                    ON CONFLICT (username) DO NOTHING
                """),
                {"password_hash": password_hash}
            )
            session.commit()
            print("OK: Usuario admin criado com sucesso!")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"ERRO ao criar admin: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("Migracao de dados para Supabase\n")
    success = migrate_users_from_backup()
    
    if success:
        print("\nOK: Migracao concluida!")
        print("O bot deve funcionar agora.")
    else:
        print("\nERRO: Migracao falhou.")
        sys.exit(1)
