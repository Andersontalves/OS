"""
Script para criar arquivo .env local para testes
Usa o mesmo banco de dados do Supabase (produção)
"""
import os
import secrets

def criar_env():
    print("🔧 Criando arquivo .env para testes locais...")
    print()
    
    # Verificar se já existe
    if os.path.exists('.env'):
        resposta = input("⚠️  Arquivo .env já existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada.")
            return
    
    # Coletar informações
    print("📝 Preencha as informações abaixo:")
    print()
    
    # DATABASE_URL (Supabase)
    print("1. DATABASE_URL do Supabase:")
    print("   (Exemplo: postgresql://postgres.xxxxx:senha@host:5432/postgres)")
    database_url = input("   DATABASE_URL: ").strip()
    if not database_url:
        print("❌ DATABASE_URL é obrigatório!")
        return
    
    # JWT_SECRET
    print()
    print("2. JWT_SECRET (chave secreta para tokens):")
    print("   (Pode gerar uma nova ou usar a existente)")
    jwt_secret = input("   JWT_SECRET (Enter para gerar automaticamente): ").strip()
    if not jwt_secret:
        jwt_secret = secrets.token_urlsafe(32)
        print(f"   ✅ Gerado automaticamente: {jwt_secret[:20]}...")
    
    # CLOUDINARY_URL
    print()
    print("3. CLOUDINARY_URL:")
    print("   (Formato: cloudinary://api_key:api_secret@cloud_name)")
    cloudinary_url = input("   CLOUDINARY_URL: ").strip()
    if not cloudinary_url:
        print("⚠️  CLOUDINARY_URL não fornecido. Você precisará configurar depois.")
    
    # Criar arquivo .env
    env_content = f"""# Configuração para TESTES LOCAIS
# Usa o mesmo banco de dados do Supabase (produção)

# Banco de Dados (Supabase)
DATABASE_URL={database_url}

# JWT Secret
JWT_SECRET={jwt_secret}

# Cloudinary
CLOUDINARY_URL={cloudinary_url}

# API
API_HOST=0.0.0.0
API_PORT=8000

# CORS
CORS_ORIGINS=["*"]
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print()
    print("✅ Arquivo .env criado com sucesso!")
    print()
    print("📋 Próximos passos:")
    print("   1. Execute a migração: python migrate_add_tipo_prazo.py")
    print("   2. Inicie o backend: python -m uvicorn app.main:app --reload")
    print()

if __name__ == "__main__":
    try:
        criar_env()
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
