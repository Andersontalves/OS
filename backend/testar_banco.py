"""
Script para testar conexão com banco de dados e verificar usuário admin
"""
import os
import sys
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

from app.database import engine, SessionLocal, Base
# Importar todos os modelos para evitar erros de relacionamento
from app.models import user, ordem_servico  # noqa: F401
from app.models.user import User
from sqlalchemy import text

print("=" * 50)
print("TESTE DE CONEXAO COM BANCO DE DADOS")
print("=" * 50)
print()

# Teste 1: Conexão básica
print("[1] Testando conexao com banco...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("[OK] Conexao com banco OK!")
except Exception as e:
    print(f"[ERRO] ERRO ao conectar ao banco: {e}")
    print()
    print("Possiveis causas:")
    print("  - Sem conexao com internet")
    print("  - DATABASE_URL incorreto no .env")
    print("  - Supabase temporariamente indisponivel")
    sys.exit(1)

print()

# Teste 2: Criar tabelas se não existirem (importante para SQLite)
print("[2] Criando/verificando tabelas...")
try:
    Base.metadata.create_all(bind=engine)
    print("[OK] Tabelas verificadas/criadas!")
except Exception as e:
    print(f"[AVISO] Aviso ao criar tabelas: {e}")

print()

# Teste 3: Verificar usuário admin
print("[3] Verificando usuario admin...")
db = SessionLocal()
try:
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print(f"[OK] Usuario admin existe (ID: {admin.id})")
        print(f"   Nome: {admin.nome}")
        print(f"   Role: {admin.role}")
    else:
        print("[INFO] Usuario admin NAO encontrado!")
        print()
        print("Criando usuario admin...")
        from app.services.auth_service import hash_password
        admin_user = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin",
            nome="Administrador do Sistema"
        )
        db.add(admin_user)
        db.commit()
        print("[OK] Usuario admin criado com sucesso!")
        print("   Usuario: admin")
        print("   Senha: admin123")
except Exception as e:
    print(f"[ERRO] ERRO ao verificar/criar admin: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

print()
print("=" * 50)
print("TESTE CONCLUIDO")
print("=" * 50)
