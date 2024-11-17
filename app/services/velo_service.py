# %%
from typing import Dict
import pandas as pd
from velodata import lib as velo
from app.core.settings import get_settings

settings = get_settings()


class VeloService:
    def __init__(self):
        self.client = velo.client(settings.VELO_API_KEY)

    def get_available_futures_products(self) -> pd.DataFrame:
        """Retrieves all available products (tickers)."""
        products = self.client.get_futures()
        data = pd.DataFrame(products)
        data['begin'] = pd.to_datetime(data['begin'], unit='ms')
        return data

    def get_historical_funding_rates_daily(self, pair: str = "BTCUSDT", exchange: str = "binance-futures") -> pd.DataFrame:
        """Retrieves daily historical funding rates for a specified product over the longest available period."""
        params = {
            'type': 'futures',
            'columns': ['funding_rate'],
            'exchanges': [exchange],
            'products': [pair],
            'begin': 0,  # Set to earliest possible timestamp
            'end': self.client.timestamp(),  # Current timestamp
            'resolution': '1d'  
        }
        
        data = self.client.get_rows(params)
        df = pd.DataFrame(data)
        df = df[['time', 'funding_rate']]
        df = df.rename(columns={'time': 'date'})
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df['funding_rate'] = df['funding_rate'].apply(lambda x: x * 100)

        return df

    def get_historical_ohlcv_daily(self, pair: str = "BTCUSDT", exchange: str = "binance-futures", from_time: int = 0, to_time: int = 0) -> pd.DataFrame:
        """Retrieves daily historical OHLCV candles for a specified product."""
        params = {
            'type': 'futures',
            'columns': ['open_price', 'high_price', 'low_price', 'close_price', 'coin_volume'],
            'exchanges': [exchange],
            'products': [pair],
            'begin': from_time * 1000,
            'end': to_time * 1000,
            'resolution': '1d'
        }
    
        return self.client.get_rows(params)


# %%

class UDFService:
    def __init__(self):
        self.velo = VeloService()

    def get_config(self):
        """UDF config endpoint"""
        return {
            "supported_resolutions": ["1D"],  # Only daily for now based on your current implementation
            "supports_group_request": False,
            "supports_search": True,
            "supports_marks": False,
            "supports_timescale_marks": False
        }

    def get_symbol_info(self, symbol: str):
        """UDF symbols endpoint"""
        # Get available products to validate symbol
        products_df = self.velo.get_available_futures_products()
        if symbol not in products_df['product'].values:
            return {"s": "error", "errmsg": "Symbol not found"}

        return {
            "symbol": symbol,
            "ticker": symbol,
            "name": symbol,
            "description": symbol,
            "type": "crypto",
            "session": "24x7",
            "timezone": "Etc/UTC",
            "exchange": products_df[products_df['product'] == symbol]['exchange'].values[0],
            "minmov": 1,
            "pricescale": 100,
            "has_intraday": False,
            "has_daily": True,
            "has_weekly_and_monthly": False
        }

    def get_history(self, symbol: str, from_time: int, to_time: int, resolution: str):
        """UDF history endpoint"""
        try:
            # Get OHLCV data
            data = self.velo.get_historical_ohlcv_daily(pair=symbol, from_time=from_time, to_time=to_time)
            
            if len(data) == 0:
                return {
                    "s": "no_data",
                    "nextTime": None
                }

            df = pd.DataFrame(data)
            
            return {
                "s": "ok",
                "t": (df['time'] // 1000).tolist(),
                "o": df['open_price'].tolist(),
                "h": df['high_price'].tolist(), 
                "l": df['low_price'].tolist(),
                "c": df['close_price'].tolist(),
                "v": df['coin_volume'].tolist()
            }

        except Exception as e:
            return {"s": "error", "errmsg": str(e)}

    def get_time(self):
        """UDF time endpoint"""
        return int(pd.Timestamp.now().timestamp())

    def search_symbols(self, query: str, limit: int):
        """UDF symbol search endpoint"""
        products_df = self.velo.get_available_futures_products()
        
        # Filter products by query
        matches = products_df[products_df['product'].str.contains(query, case=False)]
        matches = matches.head(limit)

        return [
            {
                "symbol": row['product'],
                "full_name": row['product'],
                "description": row['product'],
                "exchange": row['exchange'],
                "type": "crypto"
            }
            for _, row in matches.iterrows()
        ]