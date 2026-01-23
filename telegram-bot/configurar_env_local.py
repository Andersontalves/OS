"""
Script para configurar .env.local do bot de teste
"""
import os

def configurar_env_local():
    print("🔧 Configurando .env.local para bot de teste...")
    print()
    
    # Verificar se já existe
    if os.path.exists('.env.local'):
        resposta = input("⚠️  Arquivo .env.local já existe. Deseja sobrescrever? (s/N): ")
        if resposta.lower() != 's':
            print("❌ Operação cancelada.")
            return
    
    # Token do bot de teste
    print("1. Token do Bot de Teste:")
    print("   (Você já tem: 8558207794:AAFjF-F_bg7pAM1Gw2Vn0R2k2VLycBXlIgo)")
    token = input("   TELEGRAM_BOT_TOKEN (Enter para usar o padrão): ").strip()
    if not token:
        token = "8558207794:AAFjF-F_bg7pAM1Gw2Vn0R2k2VLycBXlIgo"
        print("   ✅ Usando token padrão do bot de teste")
    
    # API Base URL
    print()
    print("2. URL da API (backend local):")
    api_url = input("   API_BASE_URL (Enter para http://localhost:8000): ").strip()
    if not api_url:
        api_url = "http://localhost:8000"
    
    # Cloudinary
    print()
    print("3. CLOUDINARY_URL:")
    print("   (Formato: cloudinary://api_key:api_secret@cloud_name)")
    print("   (Use o mesmo da produção)")
    cloudinary_url = input("   CLOUDINARY_URL: ").strip()
    if not cloudinary_url:
        print("⚠️  CLOUDINARY_URL não fornecido. Você precisará configurar depois.")
        cloudinary_url = "cloudinary://api_key:api_secret@cloud_name"
    
    # Criar arquivo
    env_content = f"""# Configuração para BOT DE TESTE
# Token do bot de teste criado no @BotFather
TELEGRAM_BOT_TOKEN={token}

# API local (backend rodando na sua máquina)
API_BASE_URL={api_url}

# Cloudinary (use o mesmo da produção)
CLOUDINARY_URL={cloudinary_url}
"""
    
    with open('.env.local', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print()
    print("✅ Arquivo .env.local criado com sucesso!")
    print()
    print("📋 Próximo passo:")
    print("   Execute: python bot.py")
    print()

if __name__ == "__main__":
    try:
        configurar_env_local()
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
