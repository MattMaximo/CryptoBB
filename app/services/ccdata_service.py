import aiohttp
import pandas as pd
import numpy as np
import asyncio
from typing import List, Dict, Tuple
from app.core.settings import get_settings
from app.core.session_manager import SessionManager

settings = get_settings()

class CCDataService:
    def __init__(self):
        self.api_key = settings.CCDATA_API_KEY
        self.base_url = "https://data-api.cryptocompare.com"
        self.headers = {"Content-type": "application/json; charset=UTF-8"}
        self.session_manager = SessionManager()
        
        self.exchange_pairs = {
            "binance": ["BTC-USDC", "BTC-USDT"],
            "coinbase": ["BTC-USDT", "BTC-USD"],
            "bybit": ["BTC-USDE", "BTC-USDC", "BTC-USDT"],
            "okex": ["BTC-USDT", "BTC-USDC"],
            "cryptodotcom": ["BTC-USD", "BTC-USDT"],
            "upbit": ["BTC-USDT", "BTC-USDC"],
            "kraken": ["BTC-USD", "BTC-USDT"],
            "mexc": ["BTC-USDT", "BTC-USDC"],
        }

    async def _fetch_spot_data(self, exchange_pair: Tuple[str, str], interval: str = "hours", aggregate: int = 1, limit: int = 120) -> List[Dict]:
        """Fetch historical spot data for a specific exchange and trading pair."""
        exchange, pair = exchange_pair
        
        session = await self.session_manager.get_session(self.headers)
        params = {
            "market": exchange,
            "instrument": pair,
            "limit": limit,
            "aggregate": aggregate,
            "fill": "true",
            "apply_mapping": "true",
            "response_format": "JSON",
            "groups": "OHLC,VOLUME",
            "api_key": self.api_key,
        }
        
        async with session.get(f"{self.base_url}/spot/v1/historical/{interval}", params=params) as response:
            data = await response.json()
            return data['Data']

    async def get_delta_data(self) -> pd.DataFrame:
        # Create list of all exchange-pair combinations
        fetch_tasks = [(exchange, pair) 
                      for exchange, pairs in self.exchange_pairs.items() 
                      for pair in pairs]

        # Fetch all data in parallel using asyncio.gather
        tasks = [self._fetch_spot_data(task) for task in fetch_tasks]
        results = await asyncio.gather(*tasks)
        
        all_dfs = []
        for data, (exchange, pair) in zip(results, fetch_tasks):
            # Process the data into a DataFrame
            df = pd.DataFrame(data)[['TIMESTAMP', 'CLOSE', 'QUOTE_VOLUME']]
            df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
            df.columns = ['timestamp', f'{exchange}_{pair.lower()}_price', f'{exchange}_{pair.lower()}_vol']
            all_dfs.append(df)

        # Rest of the processing remains the same
        base_df = pd.DataFrame({'timestamp': all_dfs[0]['timestamp'].unique()})
        
        vwap_data = []
        for exchange in self.exchange_pairs.keys():
            exchange_dfs = [df for df in all_dfs 
                          if any(col.startswith(f'{exchange}_') for col in df.columns)]
            
            if not exchange_dfs:
                continue

            exchange_df = exchange_dfs[0]
            for df in exchange_dfs[1:]:
                exchange_df = pd.merge(exchange_df, df, on='timestamp', how='outer')

            price_cols = [col for col in exchange_df.columns if col.endswith('_price')]
            vol_cols = [col for col in exchange_df.columns if col.endswith('_vol')]

            prices = exchange_df[price_cols].values
            volumes = exchange_df[vol_cols].values
            weighted_sum = np.sum(prices * volumes, axis=1)
            total_volume = np.sum(volumes, axis=1)
            vwap = weighted_sum / total_volume

            vwap_df = pd.DataFrame({
                'timestamp': exchange_df['timestamp'],
                f'{exchange}_vwap': vwap
            })
            vwap_data.append(vwap_df)

        result_df = base_df.copy()
        for vwap_df in vwap_data:
            result_df = pd.merge(result_df, vwap_df, on='timestamp', how='outer')

        vwap_cols = [col for col in result_df.columns if col.endswith('_vwap')]
        result_df['average_price'] = result_df[vwap_cols].mean(axis=1)

        for col in vwap_cols:
            exchange = col.replace('_vwap', '')
            result_df[f'{exchange}_delta'] = (
                (result_df[col] - result_df['average_price']) / result_df['average_price']
            ) 

        delta_cols = [col for col in result_df.columns if col.endswith('_delta')]
        return result_df[['timestamp'] + delta_cols + ['average_price']]

if __name__ == "__main__":
    import time
    import asyncio
    
    async def main():
        start_time = time.time()
        ccdata_service = CCDataService()
        df = await ccdata_service._fetch_spot_data(("binance", "BTC-USDC"))
        print(df)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")

    asyncio.run(main())