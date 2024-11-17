import os
import re
import pandas as pd
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import SessionPasswordNeededError
from app.core.settings import get_settings

settings = get_settings()




class TelegramService:
    async def _initialize_client(self):
        client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        if os.path.exists(self.session_name):
            await client.start()  # Use await here
            print("Telegram client started with existing session.")
        return client
    
    def __init__(self):
        self.session_name = 'jumbocircus_session.session'
        self.api_id = settings.TELEGRAM_API_ID 
        self.api_hash = settings.TELEGRAM_API_HASH 
        
        # Initialize client without starting it immediately
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    def _initialize_client(self):
        client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        if os.path.exists(self.session_name):
            client.start()  # Automatically start the client if the session file is present
            print("Telegram client started with existing session.")
        return client


    def _extract_rank(self, message_text: str):
        if message_text:
            match = re.search(r"Coinbase Rank:\s*[><]?\s*(\d+)", message_text, re.IGNORECASE)
            return int(match.group(1)) if match else None
        return None

    async def scrape_messages(self, channel_url: str, limit=None) -> pd.DataFrame:
        messages = []
        async for message in self.client.iter_messages(channel_url, limit=limit):
            if message is None:
                break
            messages.append({
                "date": message.date,
                "rank": self._extract_rank(message.text),
                "message_id": message.id,
                "text": message.text,
                "views": message.views,
                "forwards": message.forwards,
                "reactions": message.reactions,
            })

        df = pd.DataFrame(messages)
        df.dropna(subset=['rank'], inplace=True)
        return df
    
    async def get_messages(self, channel_url: str, limit=None) -> pd.DataFrame:
        return await self.scrape_messages(channel_url, limit)
    
    async def get_coinbase_app_store_rank(self) -> pd.DataFrame:
        async with self.client:
            data = await self.get_messages("coinbaseappstore")
            if not data.empty:
                data = data[["date", "rank"]]
                data = data.sort_values("date")
            return data

