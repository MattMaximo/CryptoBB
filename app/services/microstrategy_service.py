# %%
import requests
import pandas as pd
from typing import Dict
from app.core.session_manager import SessionManager

class MicrostrategyService:
    def __init__(self):
        self.url = "https://www.mstr-tracker.com/data"
        self.session_manager = SessionManager()

    async def fetch_data(self):
        session = await self.session_manager.get_session()
        async with session.get(self.url) as response:
            return await response.json()

    async def get_prices(self):
        data = await self.fetch_data()
        df_prices = pd.DataFrame({
            'date': pd.to_datetime(data["dates"]),
            'nav_premium': pd.to_numeric(data["nav_premium"], errors='coerce'),
            'mstr_price': pd.to_numeric(data["mstr_prices"], errors='coerce'),
            'btc_price': pd.to_numeric(data["btc_prices"], errors='coerce')
        })
        return df_prices
    
    async def get_treasury_data(self):
        data = await self.fetch_data()
        df_treasury = pd.DataFrame(data['treasury_table'])
        
        df_treasury['date'] = pd.to_datetime(df_treasury['Date'])
        df_treasury['btc_balance'] = pd.to_numeric(df_treasury['BTC Balance'], errors='coerce')
        df_treasury['change'] = pd.to_numeric(df_treasury['Change'], errors='coerce')
        df_treasury['btc_per_share'] = pd.to_numeric(df_treasury['BTC per Share'], errors='coerce')
        df_treasury['cost_basis'] = pd.to_numeric(df_treasury['Cost Basis'], errors='coerce')
        df_treasury['mstr_btc'] = pd.to_numeric(df_treasury['MSTR/BTC'], errors='coerce')
        df_treasury['mstr'] = pd.to_numeric(df_treasury['MSTR'], errors='coerce')
        df_treasury['btc'] = pd.to_numeric(df_treasury['BTC'], errors='coerce')
        df_treasury['total_outstanding_shares'] = pd.to_numeric(df_treasury['Total Outstanding Shares'], errors='coerce')
        df_treasury.fillna(0, inplace=True)
        return df_treasury[['date','btc_balance', 'change', 'btc_per_share',
                           'cost_basis', 'mstr_btc', 'mstr', 'btc',
                           'total_outstanding_shares']]


# %%
