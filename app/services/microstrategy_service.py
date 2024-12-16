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
        
        column_mappings = {
            'date': 'Date',
            'btc_balance': 'BTC Balance',
            'change': 'Change', 
            'btc_per_share': 'BTC per Share',
            'cost_basis': 'Cost Basis',
            'mstr_btc': 'MSTR/BTC',
            'mstr': 'MSTR',
            'btc': 'BTC',
            'total_outstanding_shares': 'Total Outstanding Shares'
        }

        # Create new columns only if the original columns exist
        for new_col, old_col in column_mappings.items():
            if old_col in df_treasury.columns:
                if new_col == 'date':
                    df_treasury[new_col] = pd.to_datetime(df_treasury[old_col])
                else:
                    df_treasury[new_col] = pd.to_numeric(df_treasury[old_col], errors='coerce')
        
        df_treasury.fillna(0, inplace=True)
        
        # Define desired columns
        desired_columns = ['date', 'btc_balance', 'change', 'btc_per_share',
                          'cost_basis', 'mstr_btc', 'mstr', 'btc',
                          'total_outstanding_shares']
        
        # Filter to only include columns that exist in the DataFrame
        available_columns = [col for col in desired_columns if col in df_treasury.columns]
        
        return df_treasury[available_columns]


# %%
