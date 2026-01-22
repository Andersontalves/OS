"""
Script interativo para configurar Supabase do zero
Guia passo a passo completo
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def print_step(step_num, title, description):
    """Imprime um passo do guia"""
    print(f"\n{'='*60}")
    print(f"PASSO {step_num}: {title}")
    print(f"{'='*60}")
    print(description)
    input("\n⏸️  Pressione ENTER quando concluir este passo...")

def check_sqlite_backup():
    """Verifica se existe banco SQLite para backup"""
    db_path = os.path.join(os.path.dirname(__file__), "os_database.db")
    
    if os.path.exists(db_path):
        print("✅ Banco SQLite encontrado!")
        resposta = input("Deseja fazer backup antes de migrar? (s/n): ").lower()
        if resposta == 's':
            print("\n🔄 Fazendo backup...")
            os.system("python backup_sqlite.py")
            return True
    else:
        print("ℹ️  Banco SQLite não encontrado localmente.")
        print("   Se você tem dados em produção, faça backup primeiro!")
        resposta = input("Deseja continuar mesmo assim? (s/n): ").lower()
        return resposta == 's'
    
    return False

def get_supabase_connection():
    """Solicita informações do Supabase"""
    print("\n" + "="*60)
    print("CONFIGURAÇÃO DO SUPABASE")
    print("="*60)
    
    print("\n📝 Preciso da string de conexão do Supabase:")
    print("   1. Acesse: https://supabase.com")
    print("   2. Vá em: Settings → Database")
    print("   3. Copie a Connection string → URI")
    print("   4. Substitua [PASSWORD] pela sua senha")
    
    print("\n📋 Exemplo:")
    print("   postgresql://postgres.xxxxx:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")
    
    database_url = input("\n🔗 Cole a string de conexão aqui: ").strip()
    
    if not database_url.startswith("postgresql://"):
        print("❌ String inválida! Deve começar com 'postgresql://'")
        return None
    
    return database_url

def update_env_file(database_url):
    """Atualiza o arquivo .env"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    env_example_path = os.path.join(os.path.dirname(__file__), ".env.example")
    
    # Lê o .env existente ou cria novo
    env_content = ""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    elif os.path.exists(env_example_path):
        with open(env_example_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
    
    # Atualiza ou adiciona DATABASE_URL
    lines = env_content.split('\n')
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('DATABASE_URL='):
            new_lines.append(f'DATABASE_URL={database_url}')
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'\nDATABASE_URL={database_url}')
    
    # Salva
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ Arquivo .env atualizado!")

def main():
    """Fluxo principal"""
    print("🚀 Configuração do Supabase - Guia Interativo")
    print("="*60)
    print("\nEste script vai te guiar passo a passo para migrar para Supabase.")
    print("Tempo estimado: 5-10 minutos\n")
    
    input("Pressione ENTER para começar...")
    
    # Passo 1: Criar projeto no Supabase
    print_step(
        1,
        "Criar Projeto no Supabase",
        """
1. Acesse: https://supabase.com
2. Faça login (ou crie conta gratuita)
3. Clique em "New Project"
4. Preencha:
   - Name: os-sistema (ou outro nome)
   - Database Password: Crie uma senha forte (ANOTE BEM!)
   - Region: South America (São Paulo)
5. Aguarde a criação (2-3 minutos)
        """
    )
    
    # Passo 2: Obter string de conexão
    print_step(
        2,
        "Obter String de Conexão",
        """
1. No projeto Supabase, vá em: Settings → Database
2. Role até: Connection string
3. Clique em: URI
4. Copie a string completa
5. IMPORTANTE: Substitua [PASSWORD] pela senha que você criou!
        """
    )
    
    # Passo 3: Verificar backup
    print("\n" + "="*60)
    print("VERIFICAÇÃO DE BACKUP")
    print("="*60)
    has_backup = check_sqlite_backup()
    
    # Passo 4: Obter string de conexão
    database_url = get_supabase_connection()
    
    if not database_url:
        print("\n❌ Configuração cancelada.")
        return
    
    # Passo 5: Atualizar .env
    print("\n📝 Atualizando arquivo .env...")
    update_env_file(database_url)
    
    # Passo 6: Criar schema
    print("\n" + "="*60)
    print("CRIANDO SCHEMA NO SUPABASE")
    print("="*60)
    print("\n🔄 Criando tabelas no Supabase...")
    resposta = input("Deseja criar o schema agora? (s/n): ").lower()
    
    if resposta == 's':
        os.system("python init_db.py")
    
    # Passo 7: Migrar dados (se houver backup)
    if has_backup:
        print("\n" + "="*60)
        print("MIGRANDO DADOS")
        print("="*60)
        resposta = input("Deseja migrar os dados do backup agora? (s/n): ").lower()
        
        if resposta == 's':
            print("\n🔄 Migrando dados...")
            os.system("python migrate_to_supabase.py")
    
    # Passo 8: Testar conexão
    print("\n" + "="*60)
    print("TESTANDO CONEXÃO")
    print("="*60)
    resposta = input("Deseja testar a conexão agora? (s/n): ").lower()
    
    if resposta == 's':
        print("\n🔍 Testando...")
        os.system("python test_database.py")
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("   1. Se estiver usando Render/Railway:")
    print("      - Vá nas configurações do serviço")
    print("      - Adicione variável: DATABASE_URL")
    print("      - Cole a string do Supabase")
    print("      - Reinicie o serviço")
    print("\n   2. Se estiver rodando localmente:")
    print("      - O .env já está configurado")
    print("      - Reinicie o servidor")
    print("\n   3. Teste:")
    print("      - Acesse o endpoint /health")
    print("      - Teste criar uma O.S pelo bot")
    print("      - Verifique no Supabase Dashboard se os dados aparecem")
    print("\n💡 Dica: Mantenha os arquivos de backup por segurança!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
