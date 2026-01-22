import requests
import cloudinary
import cloudinary.uploader
from io import BytesIO
import config
import logging

logger_bot = logging.getLogger(__name__)


# Configure Cloudinary
if config.CLOUDINARY_URL:
    cloudinary.config(cloudinary_url=config.CLOUDINARY_URL)


def upload_photo_to_cloudinary(photo_bytes: bytes, filename: str = "photo") -> str:
    """
    Upload a photo to Cloudinary
    
    Args:
        photo_bytes: Photo data as bytes
        filename: Base filename (optional)
        
    Returns:
        str: Secure URL of the uploaded photo
    """
    try:
        result = cloudinary.uploader.upload(
            photo_bytes,
            folder="os-sistema/telegram",
            resource_type="image",
            public_id=filename,
            quality="auto:good",
            fetch_format="auto"
        )
        return result["secure_url"]
    except Exception as e:
        raise Exception(f"Erro ao fazer upload: {str(e)}")


def create_os_via_api(os_data: dict) -> dict:
    """
    Create an Ordem de Serviço via API (Authenticating as Admin)
    """
    try:
        # 1. Login to get token
        # Get base API URL by stripping /os and any trailing slashes
        clean_endpoint = config.API_ENDPOINT_CREATE_OS.rstrip("/")
        if clean_endpoint.endswith("/os"):
            base_url = clean_endpoint[:-3]
        else:
            base_url = clean_endpoint
            
        auth_url = f"{base_url}/auth/login"
        print(f"DEBUG: Bot tentando login em: {auth_url}") # Will show in Render logs
        
        login_response = requests.post(
            auth_url,
            json={"username": "admin", "password": "admin123"},
            timeout=10
        )
        
        if login_response.status_code != 200:
            raise Exception(f"Falha no login do Bot: {login_response.text}")
            
        token = login_response.json()["access_token"]
        
        # 2. Create OS with Token
        response = requests.post(
            config.API_ENDPOINT_CREATE_OS,
            json=os_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            timeout=30
        )
        
        if response.status_code == 201:
            logger_bot.info(f"✅ O.S criada com sucesso: {response.json().get('numero_os')}")
            return response.json()
        else:
            try:
                error_detail = response.json().get("detail", "Erro desconhecido")
            except:
                error_detail = response.text
            logger_bot.error(f"❌ API retornou erro {response.status_code}: {error_detail}")
            raise Exception(f"API retornou erro: {error_detail}")
    
    except requests.exceptions.RequestException as e:
        logger_bot.error(f"❌ Erro de conexão com a API: {str(e)}")
        raise Exception(f"Erro de conexão com a API: {str(e)}")
