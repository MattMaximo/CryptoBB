from typing import Dict, Optional, Union, List
import pandas as pd
import aiohttp
from app.core.settings import get_settings
from app.core.session_manager import SessionManager
from urllib.parse import urlencode
import asyncio


settings = get_settings()

class CoinGeckoService:
    def __init__(self):
        self.headers = {"accept": "application/json"}
        self.api_key = settings.COINGECKO_API_KEY
        self.session_manager = SessionManager()

    async def fetch_data(self, url: str) -> Dict:
        base_url = url + ('&' if '?' in url else '?') + f'x_cg_pro_api_key={self.api_key}'
        session = await self.session_manager.get_session(self.headers)
        async with session.get(base_url) as response:
            data = await response.json()
            
            if response.status == 200 and data:
                return data
                
            raise Exception(f"Failed to fetch data from CoinGecko API. Status: {response.status}, Response: {data}")

    async def get_coin_details(self, coin_id: str) -> Dict:
        '''
        Returns a dictionary with the coin details
        '''
        url = f"https://pro-api.coingecko.com/api/v3/coins/{coin_id}"
        return await self.fetch_data(url)

    async def get_coin_list(self, include_platform: str = "true", status: str = "active") -> pd.DataFrame:
        '''
        Fetches active coins list from CoinGecko API.
        Returns a dataframe with the following columns:
        - id
        - symbol
        - name
        - platforms
        '''
        url = f"https://pro-api.coingecko.com/api/v3/coins/list?include_platform={include_platform}&status={status}"
        data = await self.fetch_data(url)

        if include_platform:
            df = pd.DataFrame(data)
            df["platforms"] = df["platforms"].apply(
                lambda d: ", ".join(d.keys()) if isinstance(d, dict) else ""
            )
        return df
    
    async def get_coin_list_market_data(self, coin_ids: Optional[str] = None, category: Optional[str] = None) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        - id
        - symbol
        - name
        - image
        - current_price
        - market_cap
        - market_cap_rank
        - total_volume
        - price_change_percentage_1h_in_currency
        - price_change_percentage_24h_in_currency
        - price_change_percentage_7d_in_currency
        '''
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 250,
            'sparkline': 'false',
            'price_change_percentage': '1h,24h,7d,14d,30d,200d,1y'
        }
        
        if coin_ids:
            params['ids'] = coin_ids
            
        if category:
            params['category'] = category
            
        url = f"https://pro-api.coingecko.com/api/v3/coins/markets?{urlencode(params)}"
        data = await self.fetch_data(url)
        return pd.DataFrame(data)

    
    
    
    async def get_total_marketcap(self) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        - date
        - total_market_cap
        '''
        url = "https://pro-api.coingecko.com/api/v3/global/market_cap_chart?days=max"
        data = await self.fetch_data(url)
        data = data.get("market_cap_chart", {})

        market_cap_data = pd.DataFrame(
            data["market_cap"], columns=["date", "total_market_cap"]
        )
        market_cap_data["date"] = pd.to_datetime(market_cap_data["date"], unit="ms")
        return market_cap_data

    async def get_market_data(self, coin_id: Union[str, List[str]]) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        For single coin:
            - date
            - {coin_id}_price
            - {coin_id}_market_cap
            - {coin_id}_volume
        For multiple coins:
            - date
            - price
            - market_cap
            - volume
            - coingecko_id
        '''
        # Handle single coin case (maintain existing behavior)
        if isinstance(coin_id, str):
            url = f"https://pro-api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=max&interval=daily"
            data = await self.fetch_data(url)

            prices = pd.DataFrame(data["prices"], columns=["date", f"{coin_id}_price"])
            market_cap = pd.DataFrame(
                data["market_caps"], columns=["date", f"{coin_id}_market_cap"]
            )
            volume = pd.DataFrame(
                data["total_volumes"], columns=["date", f"{coin_id}_volume"]
            )

            df = prices.merge(market_cap, on="date").merge(volume, on="date")
            df["date"] = pd.to_datetime(df["date"], unit="ms")
            df = df[df["date"].dt.time == pd.to_datetime("00:00:00").time()]
            return df

        # Handle multiple coins case
        async def fetch_single_coin(cid: str) -> pd.DataFrame:
            url = f"https://pro-api.coingecko.com/api/v3/coins/{cid}/market_chart?vs_currency=usd&days=max&interval=daily"
            data = await self.fetch_data(url)
            
            prices = pd.DataFrame(data["prices"], columns=["date", "price"])
            market_cap = pd.DataFrame(data["market_caps"], columns=["date", "market_cap"])
            volume = pd.DataFrame(data["total_volumes"], columns=["date", "volume"])
            
            df = prices.merge(market_cap, on="date").merge(volume, on="date")
            df["date"] = pd.to_datetime(df["date"], unit="ms")
            df = df[df["date"].dt.time == pd.to_datetime("00:00:00").time()]
            df["coingecko_id"] = cid
            return df

        # Fetch all coins concurrently
        tasks = [fetch_single_coin(cid) for cid in coin_id]
        results = await asyncio.gather(*tasks)
        
        # Combine all dataframes
        return pd.concat(results, ignore_index=True)

    async def get_dominance(self, coin_id: str) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        - date
        - dominance
        '''
        total_market_cap = await self.get_total_marketcap()
        coin_data = await self.get_market_data(coin_id)
        coin_data = coin_data[["date", f"{coin_id}_market_cap"]]

        dominance_data = total_market_cap.merge(coin_data, on="date", how="inner")
        dominance_data["dominance"] = (
            dominance_data[f"{coin_id}_market_cap"]
            / dominance_data["total_market_cap"]
        )
        return dominance_data[["date", "dominance"]]

    async def get_vm_ratio(self, coin_id: str) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        - date
        - vm_ratio
        '''
        market_data = await self.get_market_data(coin_id)
        market_data["vm_ratio"] = market_data[f"{coin_id}_volume"] / market_data[f"{coin_id}_market_cap"]
        return market_data[["date", "vm_ratio"]]

    async def get_correlation(self, coin_id1: str, coin_id2: str, days: int = 30) -> pd.DataFrame:
        '''
        Returns a dataframe with the following columns:
        - date
        - correlation
        '''
        market_data1 = await self.get_market_data(coin_id1)
        market_data2 = await self.get_market_data(coin_id2)

        market_data1 = market_data1[["date", f"{coin_id1}_price"]]
        market_data2 = market_data2[["date", f"{coin_id2}_price"]]

        merged_data = market_data1.merge(market_data2, on="date", how="inner")
        merged_data["correlation"] = merged_data[f"{coin_id1}_price"].rolling(window=days).corr(merged_data[f"{coin_id2}_price"])
        return merged_data[["date", "correlation"]]

