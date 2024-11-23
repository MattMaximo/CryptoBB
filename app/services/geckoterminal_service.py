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
        return df[['name', 'symbol', 'price_usd', 'volume_usd', 'market_cap_usd', 'fdv_usd', 'total_supply', 'total_reserve_in_usd', 'chain', 'address']]

