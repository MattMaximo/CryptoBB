# %%
import requests
import pandas as pd

class MicrostrategyService:
    def __init__(self):
        self.url = "https://www.mstr-tracker.com/data"
        response = requests.get(self.url)
        response.raise_for_status()  # Raise exception for bad status codes
        self._data = response.json()

    def get_prices(self):
        df_prices = pd.DataFrame({
            'date': pd.to_datetime(self._data["dates"]),
            'nav_premium': pd.to_numeric(self._data["nav_premium"], errors='coerce'),
            'mstr_price': pd.to_numeric(self._data["mstr_prices"], errors='coerce'),
            'btc_price': pd.to_numeric(self._data["btc_prices"], errors='coerce')
        })
        return df_prices
    
    def get_treasury_data(self):
        df_treasury = pd.DataFrame(self._data['treasury_table'])
        
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

if __name__ == "__main__":
    microstrategy_service = MicrostrategyService()
    treasury_data = microstrategy_service.get_treasury_data()
    prices = microstrategy_service.get_prices()

# %%
