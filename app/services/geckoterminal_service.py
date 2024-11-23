from typing import Dict
import pandas as pd
import requests
from app.core.settings import get_settings

settings = get_settings()

class GeckoTerminalService:
    def __init__(self):
        self.api_key = settings.COINGECKO_API_KEY
        self.headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": self.api_key
        }

    def fetch_coin_market_data(self, network_id: str, coin_ids: str) -> pd.DataFrame:
        url = f"https://pro-api.coingecko.com/api/v3/onchain/networks/{network_id}/tokens/multi/{coin_ids}"
        response = requests.get(url, headers=self.headers)
        data = response.json()['data']

        df = pd.DataFrame(data)
        attributes_df = df['attributes'].apply(pd.Series)
        df['top_pool_id'] = df['relationships'].apply(lambda x: x['top_pools']['data'][0]['id'] if x['top_pools']['data'] else None)
        df = pd.concat([df.drop(['attributes', 'relationships'], axis=1), attributes_df], axis=1)
        df['volume_usd'] = df['volume_usd'].apply(lambda x: float(x['h24']))
        df.drop(columns=['id', 'decimals', 'image_url', 'coingecko_coin_id'], inplace=True)

        return df

    def _group_tokens_by_chain(self, tokens: Dict) -> Dict:
        tokens_by_chain = {}
        for token, info in tokens.items():
            chain = info['chain']
            address = info['address']
            if chain not in tokens_by_chain:
                tokens_by_chain[chain] = []
            tokens_by_chain[chain].append(address)
        return tokens_by_chain

    def fetch_ai_agent_market_data(self, tokens: Dict) -> pd.DataFrame:
        tokens_by_chain = self._group_tokens_by_chain(tokens)
        dfs = []
        for chain, addresses in tokens_by_chain.items():
            address_list = ','.join(addresses)
            df = self.fetch_coin_market_data(chain, address_list)
            df['chain'] = chain
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)
        df.drop(columns=['type'], inplace=True)
        return df[['name', 'symbol', 'price_usd', 'volume_usd', 'market_cap_usd', 'fdv_usd', 'total_supply', 'total_reserve_in_usd','top_pool_id', 'chain', 'address']]

    def fetch_pool_ohlcv_data(self, pool_id: str, chain: str, timeframe: str, aggregate: int) -> pd.DataFrame:
        """
        Parameters:
        - pool_id (str): The ID of the pool to fetch data for.
        - chain (str): The blockchain network (e.g., 'solana').
        - timeframe (str): The timeframe for the data. Options are:
            - 'minute': Data aggregated by minute.
            - 'hour': Data aggregated by hour.
            - 'day': Data aggregated by day.
        - aggregate (int): The aggregation interval. Options vary based on the timeframe:
            - For 'minute': 1, 5, 15
            - For 'hour': 1, 4, 12
            - For 'day': 1

        Returns:
        - pd.DataFrame: A DataFrame containing the OHLCV data with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume'].
        """
        url = f"https://pro-api.coingecko.com/api/v3/onchain/networks/{chain}/pools/{pool_id}/ohlcv/{timeframe}"
        
        params = {
            "aggregate": aggregate,
            "limit": 1000,
            "currency": "usd"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()['data']['attributes']['ohlcv_list']
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        return df

