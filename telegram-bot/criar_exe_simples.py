"""
Script para criar o executável do Bot Telegram
Usa PyInstaller para gerar um .exe único
"""

import subprocess
import sys
import os
import shutil

def main():
    print("=" * 50)
    print("  Criando EXE do Bot Telegram")
    print("=" * 50)
    print()
    
    # Diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    # 1. Instalar PyInstaller
    print("[1/4] Instalando PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print()
    
    # 2. Criar o executável
    print("[2/4] Criando executavel...")
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Um único arquivo
        "--windowed",          # Sem console (janela GUI)
        "--name", "Bot_Telegram_OS",
        "--clean",             # Limpar cache
        "bot_launcher.py"
    ]
    
    subprocess.run(cmd, check=True)
    print()
    
    # 3. Copiar arquivos necessários para dist
    print("[3/4] Copiando arquivos necessarios...")
    dist_dir = os.path.join(current_dir, "dist")
    
    files_to_copy = [
        "bot.py",
        "config.py", 
        "services.py",
        "requirements.txt"
    ]
    
    # Copiar .env se existir, senão copiar .env.example
    if os.path.exists(".env"):
        files_to_copy.append(".env")
    elif os.path.exists(".env.example"):
        shutil.copy(".env.example", os.path.join(dist_dir, ".env"))
        print("  - .env.example copiado como .env")
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, dist_dir)
            print(f"  - {file} copiado")
    
    print()
    
    # 4. Criar README
    print("[4/4] Criando instrucoes...")
    readme_content = """# Bot Telegram - Sistema O.S

## Como Usar

1. Configure o arquivo .env:
   - TELEGRAM_BOT_TOKEN = seu token do Telegram
   - API_BASE_URL = https://os-sistema-api.onrender.com
   - CLOUDINARY_URL = sua URL do Cloudinary

2. Execute Bot_Telegram_OS.exe

3. O bot vai iniciar automaticamente

4. Use os botoes:
   - Iniciar: Liga o bot
   - Parar: Desliga o bot
   - Reiniciar: Reinicia o bot
   - Limpar Logs: Limpa a area de logs

## Configuracao do .env

TELEGRAM_BOT_TOKEN=seu_token_aqui
API_BASE_URL=https://os-sistema-api.onrender.com
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

## Onde Conseguir

- TELEGRAM_BOT_TOKEN: @BotFather no Telegram
- CLOUDINARY_URL: cloudinary.com (conta gratuita)

## Dicas

- Mantenha o programa aberto para o bot funcionar
- Se travar, clique em Reiniciar
- Os logs mostram tudo que o bot esta fazendo
- As O.S. sao salvas no banco de dados Supabase
"""
    
    with open(os.path.join(dist_dir, "LEIA-ME.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  - LEIA-ME.txt criado")
    
    print()
    print("=" * 50)
    print("  EXE criado com sucesso!")
    print("=" * 50)
    print()
    print(f"O arquivo esta em: {os.path.join(dist_dir, 'Bot_Telegram_OS.exe')}")
    print()
    print("IMPORTANTE:")
    print("  - O arquivo .env deve estar na mesma pasta do .exe")
    print("  - Configure o .env antes de executar")
    print("  - Copie toda a pasta 'dist' para onde quiser")
    print()

if __name__ == "__main__":
    try:
        main()
        input("Pressione ENTER para fechar...")
    except Exception as e:
        print(f"\nERRO: {e}")
        input("Pressione ENTER para fechar...")
        sys.exit(1)
