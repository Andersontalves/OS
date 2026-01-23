"""
Script para configurar automaticamente as variáveis de ambiente no Render
via API, adicionando RENDER_API_KEY e RENDER_BOT_SERVICE_ID ao serviço os-sistema-api.
"""

import requests
import sys
import json
import codecs

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Cores para terminal (Windows compatível)
try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    # Se colorama não estiver instalado, usar strings vazias
    class Fore:
        GREEN = YELLOW = RED = BLUE = CYAN = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""

def print_success(msg):
    print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")

def print_warning(msg):
    print(f"{Fore.YELLOW}⚠️  {msg}{Style.RESET_ALL}")

def print_error(msg):
    print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")

def print_info(msg):
    print(f"{Fore.CYAN}ℹ️  {msg}{Style.RESET_ALL}")

def get_input(prompt, required=True):
    """Pede input do usuário com validação"""
    while True:
        value = input(f"{Fore.BLUE}{prompt}{Style.RESET_ALL}").strip()
        if value or not required:
            return value
        print_error("Este campo é obrigatório!")

def get_api_key():
    """Obtém e valida o API Key do Render"""
    print_info("Passo 1: API Key do Render")
    print("  1. Acesse: https://dashboard.render.com")
    print("  2. Vá em Account Settings → API Keys")
    print("  3. Clique em 'Create API Key'")
    print("  4. Copie o token (começa com 'rnd_...')\n")
    
    api_key = get_input("Cole o API Key do Render: ")
    
    if not api_key.startswith("rnd_"):
        print_warning("API Key geralmente começa com 'rnd_'. Verifique se está correto.")
        confirm = get_input("Continuar mesmo assim? (s/n): ", required=False)
        if confirm.lower() != 's':
            return None
    
    return api_key

def get_service_id(service_name, description):
    """Obtém e valida o Service ID"""
    print_info(f"\nPasso 2: Service ID do {service_name}")
    print(f"  {description}")
    print("  1. No Render Dashboard, vá no serviço")
    print("  2. Vá em Settings")
    print("  3. Role até 'Service ID'")
    print("  4. Copie o ID (formato: 'srv_...')\n")
    
    service_id = get_input(f"Cole o Service ID do {service_name}: ")
    
    if not service_id.startswith("srv_"):
        print_warning("Service ID geralmente começa com 'srv_'. Verifique se está correto.")
        confirm = get_input("Continuar mesmo assim? (s/n): ", required=False)
        if confirm.lower() != 's':
            return None
    
    return service_id

def test_api_key(api_key):
    """Testa se o API Key é válido fazendo uma requisição simples"""
    print_info("Testando API Key...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        # Tenta listar serviços para validar o token
        response = requests.get("https://api.render.com/v1/services", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_success("API Key válido!")
            return True
        elif response.status_code == 401:
            print_error("API Key inválido ou expirado!")
            return False
        else:
            print_warning(f"Resposta inesperada: {response.status_code}")
            return True  # Continua mesmo assim
    except Exception as e:
        print_error(f"Erro ao testar API Key: {e}")
        return False

def get_existing_env_vars(api_key, service_id):
    """Obtém as variáveis de ambiente existentes do serviço"""
    print_info(f"Obtendo variáveis de ambiente existentes...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        url = f"https://api.render.com/v1/services/{service_id}/env-vars"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            env_vars = response.json()
            print_success(f"Encontradas {len(env_vars)} variáveis existentes")
            return env_vars
        elif response.status_code == 404:
            print_error(f"Serviço não encontrado! Verifique o Service ID.")
            return None
        else:
            print_error(f"Erro ao obter variáveis: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Erro ao obter variáveis: {e}")
        return None

def update_env_vars(api_key, service_id, env_vars):
    """Atualiza as variáveis de ambiente do serviço"""
    print_info("Atualizando variáveis de ambiente...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        url = f"https://api.render.com/v1/services/{service_id}/env-vars"
        
        # Prepara o payload (array de objetos {key, value})
        payload = [{"key": k, "value": v} for k, v in env_vars.items()]
        
        response = requests.put(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            print_success("Variáveis de ambiente atualizadas com sucesso!")
            return True
        else:
            print_error(f"Erro ao atualizar: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Erro ao atualizar: {e}")
        return False

def main():
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
    print("🔧 Configurador Automático - Render API")
    print("="*60 + Style.RESET_ALL + "\n")
    
    # Verificar se foi passado via linha de comando
    if len(sys.argv) == 4:
        api_key = sys.argv[1]
        backend_service_id = sys.argv[2]
        bot_service_id = sys.argv[3]
        print_info("Usando parâmetros da linha de comando")
    else:
        # 1. Obter API Key
        api_key = get_api_key()
        if not api_key:
            print_error("Operação cancelada.")
            return
        
        # 2. Testar API Key
        if not test_api_key(api_key):
            print_error("Não foi possível continuar com este API Key.")
            return
        
        # 3. Obter Service ID do backend (os-sistema-api)
        backend_service_id = get_service_id(
            "os-sistema-api (Backend)",
            "Este é o serviço onde vamos adicionar as variáveis."
        )
        if not backend_service_id:
            print_error("Operação cancelada.")
            return
        
        # 4. Obter Service ID do bot (os-sistema-bot)
        bot_service_id = get_service_id(
            "os-sistema-bot (Bot Telegram)",
            "Este é o serviço que será reiniciado quando o bot estiver offline."
        )
        if not bot_service_id:
            print_error("Operação cancelada.")
            return
    
    # Testar API Key mesmo se veio da linha de comando
    if not test_api_key(api_key):
        print_error("API Key inválido!")
        return
    
    # 5. Obter variáveis existentes
    existing_vars = get_existing_env_vars(api_key, backend_service_id)
    if existing_vars is None:
        print_error("Não foi possível obter variáveis existentes.")
        return
    
    # Converter lista para dicionário
    env_dict = {}
    if isinstance(existing_vars, list):
        for var in existing_vars:
            if isinstance(var, dict) and "key" in var and "value" in var:
                env_dict[var["key"]] = var["value"]
    elif isinstance(existing_vars, dict):
        env_dict = existing_vars
    
    # 6. Adicionar/atualizar as novas variáveis
    print_info("\nAdicionando/atualizando variáveis:")
    print(f"  RENDER_API_KEY = {api_key[:10]}...")
    print(f"  RENDER_BOT_SERVICE_ID = {bot_service_id}")
    
    env_dict["RENDER_API_KEY"] = api_key
    env_dict["RENDER_BOT_SERVICE_ID"] = bot_service_id
    
    # 7. Mostrar resumo
    print(f"\n{Style.BRIGHT}Resumo das variáveis que serão configuradas:{Style.RESET_ALL}")
    print(f"Total: {len(env_dict)} variáveis")
    for key in sorted(env_dict.keys()):
        value = env_dict[key]
        if key in ["RENDER_API_KEY", "JWT_SECRET", "DATABASE_URL"]:
            # Mascarar valores sensíveis
            if len(value) > 10:
                display_value = value[:10] + "..." + value[-4:]
            else:
                display_value = "***"
        else:
            display_value = value
        print(f"  • {key} = {display_value}")
    
    # 8. Confirmar
    print_warning("\n⚠️  ATENÇÃO: Isso vai substituir TODAS as variáveis de ambiente!")
    print_warning("   Variáveis existentes serão mantidas, mas novas serão adicionadas.")
    confirm = get_input("\nContinuar? (s/n): ", required=False)
    if confirm.lower() != 's':
        print_info("Operação cancelada pelo usuário.")
        return
    
    # 9. Atualizar
    if update_env_vars(api_key, backend_service_id, env_dict):
        print_success("\n" + "="*60)
        print_success("✅ Configuração concluída com sucesso!")
        print_success("="*60)
        print_info("\nPróximos passos:")
        print("  1. O serviço os-sistema-api vai reiniciar automaticamente")
        print("  2. Aguarde 1-2 minutos")
        print("  3. Teste clicando em 'Destravar Bot' no site")
        print("  4. Se o bot estiver offline, ele será reiniciado automaticamente!")
    else:
        print_error("\nFalha ao atualizar variáveis. Verifique os erros acima.")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        print("""
🔧 Configurador Automático - Render API

Uso:
  python configurar_render_api.py
  python configurar_render_api.py <API_KEY> <BACKEND_SERVICE_ID> <BOT_SERVICE_ID>

Exemplo:
  python configurar_render_api.py rnd_xxxxx srv_yyyyy srv_zzzzz

Parâmetros:
  API_KEY              - API Key do Render (começa com rnd_...)
  BACKEND_SERVICE_ID   - Service ID do os-sistema-api (começa com srv_...)
  BOT_SERVICE_ID       - Service ID do os-sistema-bot (começa com srv_...)

Se executar sem parâmetros, o script pedirá as informações interativamente.
        """)
        sys.exit(0)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print_error("Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
