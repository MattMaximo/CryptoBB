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

def check_api_key_exists(env_var_name: str | list[str], verbose: bool = True):
    """
    Checks if specified API key(s) are set.

    Args:
        env_var_name (str | list[str]): Name of the environment variable(s) to check
        verbose (bool): Whether to print verbose output
    Returns:
        bool: True if all API keys exist and are configured, False otherwise
    """
    settings = get_settings()
    
    # ANSI color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
    # Convert single string to list for uniform processing
    env_vars = [env_var_name] if isinstance(env_var_name, str) else env_var_name
    
    all_keys_exist = True
    
    for var in env_vars:
        api_key = getattr(settings, var, None)
        
        if not api_key or api_key == "your_api_key":
            if verbose:
                print(f"{RED}API key for {var} not found or not configured.{RESET}")
            all_keys_exist = False
        else:
            if verbose:
                print(f"{GREEN}API key for {var} found.{RESET}")
    
    return all_keys_exist
