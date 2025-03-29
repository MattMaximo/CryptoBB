from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    COINGECKO_API_KEY_1: str = "your_api_key"
    COINGECKO_API_KEY_2: str = "your_api_key"
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

def check_api_key_exists(env_var_name: str):
    """
    Checks if a specified API key is set.

    Args:
        env_var_name (str): Name of the environment variable to check

    Returns:
        bool: True if API key exists and is configured, False otherwise
    """
    settings = get_settings()
    api_key = getattr(settings, env_var_name, None)

    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    if not api_key or api_key == "your_api_key":
        print(f"{RED}API key for {env_var_name} not found or not configured.{RESET}")
        return False

    print(f"{GREEN}API key for {env_var_name} found.{RESET}")
    return True
