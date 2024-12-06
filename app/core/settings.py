from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COINGECKO_API_KEY: str = "your_api_key"
    GLASSNODE_API_KEY: str = "your_api_key"
    VELO_API_KEY: str = "your_api_key"
    TELEGRAM_API_ID: str = "your_api_id"
    TELEGRAM_API_HASH: str = "your_api_hash"
    CCDATA_API_KEY: str = "your_api_key"
    ARTEMIS_API_KEY: str = "your_api_key"
    SNOWFLAKE_USER: str = "your_user"
    SNOWFLAKE_PASSWORD: str = "your_password"
    SNOWFLAKE_ACCOUNT: str = "your_account"
    SNOWFLAKE_ROLE: str = "your_role"
    SNOWFLAKE_WAREHOUSE: str = "your_warehouse"
    SNOWFLAKE_DATABASE: str = "your_database"
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings() 