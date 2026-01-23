import os
from dotenv import load_dotenv

# Carregar .env.local se existir (para testes), senão .env normal
# Isso permite ter um bot de teste separado sem interferir na produção
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
    try:
        print("[TESTE] Usando configuracao de TESTE (.env.local)")
    except UnicodeEncodeError:
        print("[TESTE] Usando configuracao de TESTE (.env.local)")
else:
    load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# API Backend
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_ENDPOINT_CREATE_OS = f"{API_BASE_URL}/api/v1/os"

# Cloudinary
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

# Validation
MAX_LOCATION_PRECISION_METERS = 5.0  # Maximum acceptable GPS precision
MIN_POWER_METER_DBM = -21.0  # Minimum acceptable power meter value
