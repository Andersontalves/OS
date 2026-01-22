import httpx
import cloudinary
import cloudinary.uploader
from io import BytesIO
import config
import logging

logger_bot = logging.getLogger(__name__)

# Configure Cloudinary
if config.CLOUDINARY_URL:
    cloudinary.config(cloudinary_url=config.CLOUDINARY_URL)


async def check_api_health() -> bool:
    """Check if the backend API is reachable"""
    try:
        base_url = config.API_BASE_URL.rstrip("/")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/", timeout=5.0)
            return response.status_code == 200
    except Exception as e:
        logger_bot.debug(f"Health check failed: {e}")
        return False


def upload_photo_to_cloudinary(photo_bytes: bytes, filename: str = "photo") -> str:
    """
    Upload a photo to Cloudinary (Sync because Cloudinary SDK is sync)
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


async def create_os_via_api(os_data: dict) -> dict:
    """
    Create an Ordem de Serviço via API (Authenticating as Admin)
    """
    async with httpx.AsyncClient(timeout=45.0) as client:
        try:
            # 1. Login to get token
            clean_endpoint = config.API_ENDPOINT_CREATE_OS.rstrip("/")
            if clean_endpoint.endswith("/os"):
                base_url = clean_endpoint[:-3]
            else:
                base_url = clean_endpoint
                
            auth_url = f"{base_url}/auth/login"
            logger_bot.info(f"🔑 Bot iniciando login em: {auth_url}")
            
            login_response = await client.post(
                auth_url,
                json={"username": "admin", "password": "admin123"}
            )
            
            logger_bot.info(f"📡 Resposta Login: {login_response.status_code}")
            
            if login_response.status_code != 200:
                logger_bot.error(f"❌ Falha no login do Bot: {login_response.text}")
                raise Exception("Falha na autenticação com o servidor.")
                
            token = login_response.json()["access_token"]
            logger_bot.info("✅ Token obtido com sucesso.")
            
            # 2. Create OS with Token
            logger_bot.info(f"📤 Enviando O.S para: {config.API_ENDPOINT_CREATE_OS}")
            response = await client.post(
                config.API_ENDPOINT_CREATE_OS,
                json=os_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            logger_bot.info(f"📡 Resposta Criação O.S: {response.status_code}")
            
            if response.status_code == 201:
                res_json = response.json()
                logger_bot.info(f"✅ O.S criada com sucesso: {res_json.get('numero_os')}")
                return res_json
            else:
                try:
                    error_detail = response.json().get("detail", "Erro desconhecido")
                except:
                    error_detail = response.text
                logger_bot.error(f"❌ API retornou erro {response.status_code}: {error_detail}")
                raise Exception(f"Servidor retornou erro: {error_detail}")
        
        except httpx.TimeoutException:
            logger_bot.error("❌ Timeout ao conectar com a API")
            raise Exception("O servidor demorou muito para responder. Tente novamente.")
        except httpx.RequestError as e:
            logger_bot.error(f"❌ Erro de conexão com a API: {str(e)}")
            raise Exception("Não foi possível conectar ao servidor. Tente novamente em instantes.")
        except Exception as e:
            logger_bot.error(f"❌ Erro inesperado: {str(e)}")
            raise e
