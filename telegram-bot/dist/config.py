import os
from dotenv import load_dotenv

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
