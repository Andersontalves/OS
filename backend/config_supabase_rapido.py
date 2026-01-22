"""
Configuração rápida do Supabase - apenas cole a string de conexão
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def configurar_supabase():
    """Configura Supabase rapidamente"""
    print("🚀 Configuração Rápida do Supabase")
    print("="*60)
    
    print("\n📋 Você já tem o projeto criado no Supabase!")
    print("\n📝 Cole a string de conexão abaixo.")
    print("   (Substitua [YOUR-PASSWORD] pela sua senha)")
    print("\n💡 Dica: Se aparecer aviso IPv4, use Session Pooler (porta 6543)")
    
    database_url = input("\n🔗 Cole a string de conexão: ").strip()
    
    if not database_url:
        print("❌ String vazia!")
        return False
    
    if not database_url.startswith("postgresql://"):
        print("❌ String inválida! Deve começar com 'postgresql://'")
        return False
    
    # Verifica se tem [YOUR-PASSWORD]
    if "[YOUR-PASSWORD]" in database_url:
        print("\n⚠️  ATENÇÃO: Você precisa substituir [YOUR-PASSWORD] pela senha real!")
        print("   Exemplo: postgresql://postgres:minhasenha123@host:5432/postgres")
        resposta = input("\nDeseja continuar mesmo assim? (s/n): ").lower()
        if resposta != 's':
            return False
    
    # Atualiza .env
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    
    # Lê .env existente ou cria novo
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # Atualiza DATABASE_URL
    lines = env_content.split('\n') if env_content else []
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={database_url}')
            updated = True
        elif line.strip() and not line.startswith('#'):
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'DATABASE_URL={database_url}')
    
    # Salva
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"\n✅ Arquivo .env atualizado!")
    print(f"   DATABASE_URL configurado")
    
    # Pergunta se quer criar schema
    print("\n" + "="*60)
    print("CRIAR SCHEMA NO SUPABASE")
    print("="*60)
    resposta = input("Deseja criar as tabelas no Supabase agora? (s/n): ").lower()
    
    if resposta == 's':
        print("\n🔄 Criando tabelas...")
        os.system("python init_db.py")
    
    # Pergunta se quer testar
    print("\n" + "="*60)
    print("TESTAR CONEXÃO")
    print("="*60)
    resposta = input("Deseja testar a conexão agora? (s/n): ").lower()
    
    if resposta == 's':
        print("\n🔍 Testando...")
        os.system("python test_database.py")
    
    # Resumo
    print("\n" + "="*60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("\n1. Se estiver usando Render/Railway:")
    print("   - Vá em: Configurações → Environment Variables")
    print("   - Adicione: DATABASE_URL")
    print("   - Cole a mesma string de conexão")
    print("   - Reinicie o serviço")
    print("\n2. Se estiver rodando localmente:")
    print("   - O .env já está configurado")
    print("   - Reinicie o servidor: python -m uvicorn app.main:app")
    print("\n3. Teste:")
    print("   - Acesse: http://localhost:8000/health")
    print("   - Teste criar uma O.S pelo bot")
    print("   - Verifique no Supabase Dashboard")
    
    return True

if __name__ == "__main__":
    try:
        configurar_supabase()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
