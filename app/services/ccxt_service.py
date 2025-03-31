import ccxt.async_support as ccxt
import pandas as pd
import asyncio
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import time

class CCXTService:
    def __init__(self):
        self.exchanges_cache = {}
        
    def get_exchange(self, exchange_id: str) -> ccxt.Exchange:
        """Get or create an exchange instance."""
        if exchange_id not in self.exchanges_cache:
            # Create exchange instance with reasonable defaults
            exchange_class = getattr(ccxt, exchange_id)
            self.exchanges_cache[exchange_id] = exchange_class({
                'enableRateLimit': True,
                'timeout': 30000,
            })
        return self.exchanges_cache[exchange_id]
        
    async def close_exchanges(self):
        """Close all exchange connections."""
        for exchange in self.exchanges_cache.values():
            await exchange.close()
        self.exchanges_cache = {}
    
    async def get_exchanges(self) -> List[str]:
        """Get list of supported exchanges."""
        return ccxt.exchanges
    
    async def get_symbols(self, exchange_id: str) -> List[Dict[str, Any]]:
        """Get all symbols from an exchange."""
        try:
            exchange = self.get_exchange(exchange_id)
            await exchange.load_markets()
            
            symbols = []
            for symbol, market in exchange.markets.items():
                # Skip non-spot markets if needed
                if 'spot' not in market['type']:
                    continue
                    
                symbols.append({
                    'symbol': symbol.replace('/', '-'),  # Use dash for TradingView
                    'full_name': f"{exchange_id}:{symbol.replace('/', '-')}",
                    'description': f"{market['base']}/{market['quote']}",
                    'exchange': exchange_id,
                    'ticker': symbol,
                    'type': 'crypto'
                })
                
            return symbols
            
        except Exception as e:
            print(f"Error fetching symbols from {exchange_id}: {e}")
            return []
        
    async def get_bars(
        self, 
        exchange_id: str, 
        symbol: str, 
        timeframe: str, 
        since: Optional[int] = None,
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """Get OHLCV data from an exchange."""
        try:
            exchange = self.get_exchange(exchange_id)
            
            # Fetch OHLCV data
            ohlcv = await exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                since=since,
                limit=limit
            )
            
            # Return empty DataFrame if no data
            if not ohlcv:
                return pd.DataFrame()
                
            # Convert to DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            return df
            
        except Exception as e:
            print(f"Error fetching OHLCV data from {exchange_id} for {symbol}: {e}")
            return pd.DataFrame()