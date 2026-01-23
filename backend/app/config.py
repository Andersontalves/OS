from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = "sqlite:///./os_database.db"
    
    # JWT
    jwt_secret: str = "seu_secret_super_seguro_aqui_minimo_32_caracteres"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Cloudinary
    cloudinary_url: str = ""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # CORS
    cors_origins: list = ["http://localhost:8080", "http://localhost:3000", "*"]
    
    # Render API (opcional - para reiniciar bot)
    render_api_key: str = ""
    render_bot_service_id: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

def clear_settings_cache():
    """Clear settings cache to force reload"""
    get_settings.cache_clear()
