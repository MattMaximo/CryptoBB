from telethon import TelegramClient
from app.core.settings import get_settings

settings = get_settings()

# Replace 'your_api_id' and 'your_api_hash' with your API credentials
api_id = settings.TELEGRAM_API_ID
api_hash = settings.TELEGRAM_API_HASH

# Choose a session name (the session file will be saved as 'your_session_name.session')
session_name = 'jumbocircus_session'

# Start the client and prompt login
with TelegramClient(session_name, api_id, api_hash) as client:
    print("Session file created successfully!")
