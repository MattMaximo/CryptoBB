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
    
    def basis(self, coin='BTC', begin=None, resolution='1d') -> pd.DataFrame:
        """
        Return the basis for the specified coin by exchange.
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
            'columns': ['3m_basis_ann'],
            'coins': [coin],
            'begin': begin_timestamp,
            'end': self.client.timestamp(),  # current timestamp
            'resolution': resolution
        }

        # Fetch data
        df = self.client.get_rows(params)
        df.time = pd.to_datetime(df.time, unit='ms')

        return df

# %%
