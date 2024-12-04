# %%

from typing import Dict
import pandas as pd
import aiohttp
from app.core.session_manager import SessionManager

class AaveService:
    def __init__(self):
        self.session_manager = SessionManager()

    async def fetch_data(self, url: str) -> Dict:
        session = await self.session_manager.get_session()
        async with session.get(url) as response:
            return await response.json()

    async def get_lending_pool_history(
        self,
        pool: str,
        start_date: int = 0,
        interval_hours: int = 24
    ) -> pd.DataFrame:
        url = f"https://aave-api-v2.aave.com/data/rates-history?reserveId={pool}&from={start_date}&resolutionInHours={interval_hours}"
        data = await self.fetch_data(url)
        
        df = pd.DataFrame(data)

        # Create datetime column with explicit format
        df['datetime'] = pd.to_datetime(
            df['x'].apply(lambda x: f"{x['year']}-{x['month']:02d}-{x['date']:02d} {x['hours']:02d}:00:00"), 
            format="%Y-%m-%d %H:%M:%S",  # Specifying format directly
            errors='coerce'
        )

        # Drop any rows where 'datetime' is NaT due to parsing issues
        df = df.dropna(subset=['datetime']).drop(columns='x')
        df.rename(columns={'datetime': 'date'}, inplace=True)

        return df



# %%