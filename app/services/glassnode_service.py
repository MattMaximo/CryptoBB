
import pandas as pd
import requests
from typing import Dict
from app.core.settings import get_settings
from app.core.session_manager import SessionManager
settings = get_settings()



class GlassnodeService:
    def __init__(self):
        self.api_key = settings.GLASSNODE_API_KEY
        self.session_manager = SessionManager()

    async def fetch_data(self, url: str, params: Dict = None) -> Dict:
        session = await self.session_manager.get_session()
        async with session.get(url, params=params) as response:
            return await response.json()

    async def get_price(
        self,
        asset: str = 'btc',
        since: str = None,
        until: str = None,
        frequency: str = "24h",
        format: str = "JSON",
        timestamp_format: str = "humanized",
    ) -> pd.DataFrame:
        
        url = "https://api.glassnode.com/v1/metrics/market/price_usd_close"
        params = {
            "a": asset,
            #"s": since,
            #"u": until,
            "i": frequency,
            "f": format,
            "timestamp_format": timestamp_format,
            "api_key": self.api_key,
        }


        data = await self.fetch_data(url, params=params)

        df = pd.DataFrame(data)
        df.columns = ["date", "price"]

        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df

    async def get_lth_net_change(
        self,
        asset: str = 'btc',
        since: str = None,
        until: str = None,
        frequency: str = "24h",
        format: str = "JSON",
        timestamp_format: str = "humanized",
    ) -> pd.DataFrame:
        
        url = "https://api.glassnode.com/v1/metrics/supply/lth_net_change"
        params = {
            "a": asset,
            #'s': since,
            #'u': until,
            "i": frequency,
            "f": format,
            "timestamp_format": timestamp_format,
            "api_key": self.api_key,
        }

        data = await self.fetch_data(url, params=params)

        df = pd.DataFrame(data)
        df.columns = ["date", "lth_net_change"]

        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df
    
    async def get_lth_supply(
        self,
        asset: str = 'btc',
        since: str = None,
        until: str = None,
        frequency: str = "24h",
        format: str = "JSON",
        timestamp_format: str = "humanized",
    ) -> pd.DataFrame:
        
        url = "https://api.glassnode.com/v1/metrics/supply/lth_sum"
        params = {
            "a": asset,
            #'s': since,
            #'u': until,
            "i": frequency,
            "f": format,
            "timestamp_format": timestamp_format,
            "api_key": self.api_key,
        }

        data = await self.fetch_data(url, params=params)

        df = pd.DataFrame(data)
        df.columns = ["date", "lth_supply"]

        df["date"] = pd.to_datetime(df["date"]).dt.date

        return df

    async def mvrv_zscore(
        self,
        asset: str = 'btc',
        since: str = None,
        until: str = None,
        frequency: str = "24h",
        format: str = "JSON",
        timestamp_format: str = "humanized",
    ) -> pd.DataFrame:
        
        url = " https://api.glassnode.com/v1/metrics/market/mvrv_z_score"
        params = {
            "a": asset,
            #'s': since,
            #'u': until,
            "i": frequency,
            "f": format,
            "timestamp_format": timestamp_format,
            "api_key": self.api_key,
        }

        data = await self.fetch_data(url, params=params)

        df = pd.DataFrame(data)
        df.columns = ["date", "mvrv_zscore"]

        df["date"] = pd.to_datetime(df["date"]).dt.date
        df['mvrv_zscore'] = pd.to_numeric(df['mvrv_zscore'], errors='coerce')

        return df

    async def lth_nupl(
        self,
        asset: str = 'btc',
        since: str = None,
        until: str = None,
        frequency: str = "24h",
        format: str = "JSON",
        timestamp_format: str = "humanized",
    ) -> pd.DataFrame:
        
        url = "https://api.glassnode.com/v1/metrics/indicators/nupl_more_155_account_based"
        params = {
            "a": asset,
            #'s': since,
            #'u': until,
            "i": frequency,
            "f": format,
            "timestamp_format": timestamp_format,
            "api_key": self.api_key,
        }

        data = await self.fetch_data(url, params=params)

        df = pd.DataFrame(data)
        df.columns = ["date", "lth_nupl"]

        df["date"] = pd.to_datetime(df["date"]).dt.date
        df['lth_nupl'] = pd.to_numeric(df['lth_nupl'], errors='coerce')

        return df



# %%
 

