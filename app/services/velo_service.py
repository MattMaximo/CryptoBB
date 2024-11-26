# %%
from typing import Dict
import pandas as pd
from velodata import lib as velo
from app.core.settings import get_settings
from app.assets.annualization_intervals import intervals_per_year

settings = get_settings()


class VeloService:
    def __init__(self):
        self.client = velo.client(settings.VELO_API_KEY)
    
    def get_ohlcv(self, symbol: str, exchange: str, resolution: str = "10m") -> pd.DataFrame:
        """
        Get OHLCV data for a given symbol and exchange.
        
        Parameters:
        - symbol: Trading pair symbol
        - exchange: Exchange name
        - resolution: Time resolution (m, h, d, w, or M)
        
        Returns:
        - DataFrame with OHLCV data
        """

        day_in_ms = 1000 * 60 * 60 * 24

        params = {
            'type': 'spot',
            'columns': ['open_price', 'high_price', 'low_price', 'close_price', 'coin_volume'],
            'exchanges': [exchange],
            'products': [symbol],
            'begin': int(self.client.timestamp() - day_in_ms * 365),
            'end': int(self.client.timestamp()),
            'resolution': resolution
        }

        df = self.client.get_rows(params)

        return df[['time', 'open_price', 'high_price', 'low_price', 'close_price', 'coin_volume']]

    def get_futures_products(self) -> pd.DataFrame:
        """Retrieves all available products (tickers)."""
        products = self.client.get_futures()
        data = pd.DataFrame(products)
        data['begin'] = pd.to_datetime(data['begin'], unit='ms')
        return data
    
    def get_spot_products(self) -> pd.DataFrame:
        """Retrieves all available products (tickers)."""
        products = self.client.get_spot()
        data = pd.DataFrame(products)
        return data
    
    def get_options_products(self) -> pd.DataFrame:
        """Retrieves all available products (tickers)."""
        products = self.client.get_options()
        data = pd.DataFrame(products)
        return data


    def oi_weighted_funding_rate(self, coin='BTC', begin=None, resolution='1d') -> pd.DataFrame:
        """
        Calculate the open interest (OI) weighted funding rate for the specified coin.

        Parameters:
        - coin: Coin symbol (e.g., 'SOL').
        - begin: Start time as a string in 'YYYY-MM-DD' format.
        - resolution: Data resolution (e.g., '1m', '15m', '1h', '8h', '1d', '1w').

        Returns:
        - DataFrame with OI-weighted funding rate and annualized funding rate.
        """
        if begin is None or begin == '' or begin == "None":
            # Get futures and grab earliest date
            future = self.client.get_futures()
            df = pd.DataFrame(future)
            df = df[df['coin'] == coin]
            begin_timestamp = int(df.begin.min())
        else:
            begin_timestamp = int(pd.Timestamp(begin).timestamp() * 1000)

        params = {
            'type': 'futures',
            'columns': ['funding_rate', 'coin_open_interest_close', 'close_price'],
            'exchanges': ['binance-futures', 'bybit', 'okex-swap', 'hyperliquid'],
            'coins': [coin],
            'begin': begin_timestamp,
            'end': self.client.timestamp(),  # Current timestamp
            'resolution': resolution
        }

        # Fetch data
        df = self.client.get_rows(params)
        df.time = pd.to_datetime(df.time, unit='ms')

        # Calculate OI-weighted funding rate
        df['oi_weighted_funding_rate'] = df['funding_rate'] * df['coin_open_interest_close']
        df = df.groupby(df['time']).agg({
            'close_price': 'mean',
            'oi_weighted_funding_rate': 'sum',
            'coin_open_interest_close': 'sum'
        }).reset_index()
        df['oi_weighted_funding_rate'] = df['oi_weighted_funding_rate'] / df['coin_open_interest_close']

        df['oi_weighted_funding_rate_annualized'] = df['oi_weighted_funding_rate'] * intervals_per_year.get(resolution, 365)
        return df[['time', 'oi_weighted_funding_rate_annualized', 'close_price']]

    def funding_rates(self, coin='BTC', begin=None, resolution='1d') -> pd.DataFrame:
        """
        Return the funding rate for the specified coin by exchange.

        Parameters:
        - coin: Coin symbol (e.g., 'SOL').
        - begin: Start time as a string in 'YYYY-MM-DD' format.
        - resolution: Data resolution (e.g., '1m', '15m', '1h', '8h', '1w').

        Returns:
        - DataFrame with funding rate by exchange.
        """
        if begin is None or begin == '' or begin == "None":
            # get futures and grab earliest date
            future = self.client.get_futures()
            df = pd.DataFrame(future)
            df = df[df['coin'] == coin]
            begin_timestamp = int(df.begin.min())
        else:
            begin_timestamp = int(pd.Timestamp(begin).timestamp() * 1000)

        params = {
            'type': 'futures',
            'columns': ['funding_rate'],
            'exchanges': ['binance-futures', 'bybit', 'okex-swap', 'hyperliquid'],
            'coins': [coin],
            'begin': begin_timestamp,
            'end': self.client.timestamp(),  # current timestamp
            'resolution': resolution
        }

        # Fetch data
        df = self.client.get_rows(params)
        df.time = pd.to_datetime(df.time, unit='ms')

        # Annualize the funding rate
        df['annualized_funding_rate'] = df['funding_rate'] * intervals_per_year.get(resolution, 365)

        return df[['time', 'annualized_funding_rate', 'exchange']]
    
    def liquidations(self, coin='BTC', begin=None, resolution='1d') -> pd.DataFrame:
        """
        Return the liquidations for the specified coin by exchange.

        Parameters:
        - coin: Coin symbol (e.g., 'SOL').
        - begin: Start time as a string in 'YYYY-MM-DD' format.
        - resolution: Data resolution (e.g., '1m', '15m', '1h', '8h', '1w').

        Returns:
        - DataFrame with liquidations by exchange.
        """
        if begin is None or begin == '' or begin == "None":
            # get futures and grab earliest date
            future = self.client.get_futures()
            df = pd.DataFrame(future)
            df = df[df['coin'] == coin]
            begin_timestamp = int(df.begin.min())
        else:
            begin_timestamp = int(pd.Timestamp(begin).timestamp() * 1000)

        params = {
            'type': 'futures',
            'columns': ['close_price', 'buy_liquidations_dollar_volume', 'sell_liquidations_dollar_volume'],
            'exchanges': ['binance-futures', 'bybit', 'okex-swap', 'hyperliquid'],
            'coins': [coin],
            'begin': begin_timestamp,
            'end': self.client.timestamp(),  # current timestamp
            'resolution': resolution
        }

        # Fetch data
        df = self.client.get_rows(params)
        df.time = pd.to_datetime(df.time, unit='ms')

        return df[['time', 'close_price', 'buy_liquidations_dollar_volume', 'sell_liquidations_dollar_volume', 'exchange']]

    def open_interest(self, coin='BTC', begin=None, resolution='1d') -> pd.DataFrame:
        """
        Return the open interest (OI) for the specified coin by exchange.

        Parameters:
        - coin: Coin symbol (e.g., 'SOL').
        - begin: Start time as a string in 'YYYY-MM-DD' format.
        - resolution: Data resolution (e.g., '1m', '15m', '1h', '8h', '1w').

        Returns:
        - DataFrame with OI by exchange.
        """
        if begin is None or begin == '' or begin == "None":
            # get futures and grab earliest date
            future = self.client.get_futures()
            df = pd.DataFrame(future)
            df = df[df['coin'] == coin]
            begin_timestamp = int(df.begin.min())
        else:
            begin_timestamp = int(pd.Timestamp(begin).timestamp() * 1000)

        params = {
            'type': 'futures',
            'columns': ['dollar_open_interest_close', 'close_price'],
            'exchanges': ['binance-futures', 'bybit', 'okex-swap', 'hyperliquid'],
            'coins': [coin],
            'begin': begin_timestamp,
            'end': self.client.timestamp(),  # current timestamp
            'resolution': resolution
        }

        # Fetch data
        df = self.client.get_rows(params)
        df.time = pd.to_datetime(df.time, unit='ms')

        return df[['time', 'dollar_open_interest_close', 'close_price', 'exchange']]

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