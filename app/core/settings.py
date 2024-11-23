from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COINGECKO_API_KEY: str = "your_api_key"
    GLASSNODE_API_KEY: str = "your_api_key"
    VELO_API_KEY: str = "your_api_key"
    TELEGRAM_API_ID: str = "your_api_id"
    TELEGRAM_API_HASH: str = "your_api_hash"
    CCDATA_API_KEY: str = "your_api_key"
    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings() 