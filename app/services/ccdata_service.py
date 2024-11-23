import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple

class CCDataService:
    def __init__(self):
        self.api_key = "161f5458d9b2a02db48ebf0008d539799e70176363d1205a09c9e6cecad800c5"
        self.base_url = "https://data-api.cryptocompare.com"
        self.headers = {"Content-type": "application/json; charset=UTF-8"}
        
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

    def _fetch_spot_data(self, exchange_pair: Tuple[str, str]) -> List[Dict]:
        """Fetch historical spot data for a specific exchange and trading pair."""
        exchange, pair = exchange_pair
        
        response = requests.get(
            url=f"{self.base_url}/spot/v1/historical/hours",
            params={
                "market": exchange,
                "instrument": pair,
                "limit": 120,
                "aggregate": 1,
                "fill": "true",
                "apply_mapping": "true",
                "response_format": "JSON",
                "groups": "OHLC,VOLUME",
                "api_key": self.api_key,
            },
            headers=self.headers,
        )

        return response.json()['Data']

    def get_delta_data(self) -> pd.DataFrame:
        # Create list of all exchange-pair combinations
        fetch_tasks = [(exchange, pair) 
                      for exchange, pairs in self.exchange_pairs.items() 
                      for pair in pairs]

        # Fetch all data in parallel
        all_dfs = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_pair = {executor.submit(self._fetch_spot_data, task): task 
                            for task in fetch_tasks}
            
            for future in as_completed(future_to_pair):
                data = future.result()
                exchange, pair = future_to_pair[future]
                
                # Process the data into a DataFrame
                df = pd.DataFrame(data)[['TIMESTAMP', 'CLOSE', 'QUOTE_VOLUME']]
                df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], unit='s')
                df.columns = ['timestamp', f'{exchange}_{pair.lower()}_price', f'{exchange}_{pair.lower()}_vol']
                all_dfs.append(df)

        # Create a base timestamp DataFrame
        base_df = pd.DataFrame({'timestamp': all_dfs[0]['timestamp'].unique()})
        
        # Calculate VWAP for each exchange
        vwap_data = []
        for exchange in self.exchange_pairs.keys():
            exchange_dfs = [df for df in all_dfs 
                          if any(col.startswith(f'{exchange}_') for col in df.columns)]
            
            if not exchange_dfs:
                continue

            # Merge all pairs for this exchange
            exchange_df = exchange_dfs[0]
            for df in exchange_dfs[1:]:
                exchange_df = pd.merge(exchange_df, df, on='timestamp', how='outer')

            price_cols = [col for col in exchange_df.columns if col.endswith('_price')]
            vol_cols = [col for col in exchange_df.columns if col.endswith('_vol')]

            # Vectorized VWAP calculation
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

        # Merge all VWAP data
        result_df = base_df.copy()
        for vwap_df in vwap_data:
            result_df = pd.merge(result_df, vwap_df, on='timestamp', how='outer')

        # Calculate average price and deltas
        vwap_cols = [col for col in result_df.columns if col.endswith('_vwap')]
        result_df['average_price'] = result_df[vwap_cols].mean(axis=1)

        # Vectorized delta calculations
        for col in vwap_cols:
            exchange = col.replace('_vwap', '')
            result_df[f'{exchange}_delta'] = (
                (result_df[col] - result_df['average_price']) / result_df['average_price']
            ) 

        # Select only timestamp and delta columns
        delta_cols = [col for col in result_df.columns if col.endswith('_delta')]
        return result_df[['timestamp'] + delta_cols + ['average_price']]

if __name__ == "__main__":
    import time
    start_time = time.time()
    ccdata_service = CCDataService()
    delta_df = ccdata_service.get_delta_data()
    print(delta_df)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")