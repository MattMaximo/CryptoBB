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
            "instrument": pair,
            "market": exchange,
            "limit": limit,
            "aggregate": aggregate,
            "fill": "true",
            "apply_mapping": "true",
            "response_format": "JSON",
            "groups": "OHLC,VOLUME",
            "api_key": self.api_key
        }
        
        try:
            endpoint = "days" if interval == "day" else interval
            url = f"{self.base_url}/spot/v1/historical/{endpoint}"
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return []
                
                data = await response.json()
                if 'Data' not in data or not data['Data']:
                    return []
                
                return data['Data']
                
        except Exception:
            return []

    async def _fetch_exchange_instruments(self, exchange: str, pairs: List[str] = None) -> List[str]:
        '''
        Fetches all active instruments for a given exchange and optionally filters by pairs.

        Args:
            exchange: str - Required. The exchange to fetch instruments for (e.g., "binance")
            pairs: List[str] - Optional. List of pairs to filter by (e.g., ["BTC-USDT"])

        Returns:
            List[str]: List of mapped instruments (e.g., ["BTC-USDT", "ETH-USDT", ...])
        '''
        session = await self.session_manager.get_session(self.headers)
        params = {
            "instrument_status": "ACTIVE",
            "market": exchange,
            "api_key": self.api_key
        }
        
        if pairs:
            params["instruments"] = ",".join(pairs)
        
        async with session.get(f'{self.base_url}/spot/v1/markets/instruments', params=params) as response:
            data = await response.json()
            instruments = []
            
            if exchange not in data['Data']:
                return instruments
                
            exchange_instruments = data['Data'][exchange].get('instruments', {})
            for instrument_info in exchange_instruments.values():
                mapped_instrument = instrument_info.get('MAPPED_INSTRUMENT')
                if mapped_instrument:
                    instruments.append(mapped_instrument)
            
            return instruments

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

    async def get_total_exchange_volume(self, exchange: str) -> pd.DataFrame:
        instruments = await self._fetch_exchange_instruments(exchange)
        
        if not instruments:
            return pd.DataFrame(columns=['timestamp', 'total_volume'])
        
        tasks = [
            self._fetch_spot_data(
                (exchange, instrument),
                interval='day',
                aggregate=1,
                limit=1000
            ) 
            for instrument in instruments
        ]
        
        results = await asyncio.gather(*tasks)
        
        all_dfs = []
        for data, instrument in zip(results, instruments):
            if not data:
                continue
                
            try:
                df = pd.DataFrame(data)[['TIMESTAMP', 'QUOTE_VOLUME']]
                df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
                df.columns = ['timestamp', f'volume_{instrument.lower()}']
                all_dfs.append(df)
            except Exception:
                continue
            
        if not all_dfs:
            return pd.DataFrame(columns=['timestamp', 'total_volume'])
            
        result_df = all_dfs[0]
        for df in all_dfs[1:]:
            result_df = pd.merge(result_df, df, on='timestamp', how='outer')
            
        volume_cols = [col for col in result_df.columns if col.startswith('volume_')]
        result_df['total_volume'] = result_df[volume_cols].sum(axis=1)
        
        return result_df[['timestamp', 'total_volume']].sort_values('timestamp')


    
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