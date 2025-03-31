from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
import time
import math
from app.services.ccxt_service import CCXTService
from app.core.registry import register_widget

udf_router = APIRouter()
ccxt_service = CCXTService()

# UDF Configuration endpoints

class UDFSearchResult(BaseModel):
    symbol: str
    full_name: str
    description: str
    exchange: str
    ticker: str
    type: str

class UDFBar(BaseModel):
    s: str
    errmsg: Optional[str] = None
    t: Optional[List[int]] = None
    c: Optional[List[float]] = None
    o: Optional[List[float]] = None
    h: Optional[List[float]] = None
    l: Optional[List[float]] = None
    v: Optional[List[float]] = None
    nextTime: Optional[int] = None

class ResolutionEnum(str):
    ONE_MINUTE = "1"
    FIVE_MINUTES = "5"
    FIFTEEN_MINUTES = "15"
    THIRTY_MINUTES = "30"
    ONE_HOUR = "60"
    FOUR_HOURS = "240"
    ONE_DAY = "1D"
    ONE_WEEK = "1W"
    ONE_MONTH = "1M"

# Helper functions
def resolution_to_timeframe(resolution: str) -> str:
    timeframe_map = {
        "1": "1m",
        "5": "5m", 
        "15": "15m", 
        "30": "30m",
        "60": "1h", 
        "240": "4h", 
        "1D": "1d", 
        "D": "1d",
        "1W": "1w", 
        "W": "1w",
        "1M": "1M",
        "M": "1M"
    }
    return timeframe_map.get(resolution, "1h")

@udf_router.get("/config")
@register_widget({
    "name": "Advanced Charting",
    "description": "Advanced charting historical data from any exchange using ccxt",
    "type": "advanced_charting",
    "endpoint": "/udf",
    "gridData": {
        "w": 20,
        "h": 20
    },
    "data": {
        "defaultSymbol": "BTC-USDT",
        "updateFrequency": 60000
    }
})
async def get_config():
    """UDF config endpoint."""
    exchanges = [{"value": "", "name": "All Exchanges", "desc": ""}]
    
    # Get list of available exchanges from CCXT
    ccxt_exchanges = await ccxt_service.get_exchanges()
    for exchange_id in ccxt_exchanges:
        exchanges.append({
            "value": exchange_id,
            "name": exchange_id.capitalize(),
            "desc": exchange_id.capitalize()
        })
    
    return {
        "supported_resolutions": ["1", "5", "15", "30", "60", "240", "1D", "1W", "1M"],
        "supports_group_request": False,
        "supports_marks": False,
        "supports_search": True,
        "supports_timescale_marks": False,
        "supports_time": True,
        "exchanges": exchanges,
        "symbols_types": [
            {"name": "All types", "value": ""},
            {"name": "Crypto", "value": "crypto"}
        ]
    }

@udf_router.get("/time")
async def get_time():
    """Server time in seconds (UTC)."""
    return int(time.time())

@udf_router.get("/search", response_model=List[UDFSearchResult])
async def search_symbols(
    query: str = Query("", description="Search query"),
    limit: int = Query(30, description="Limit of results"),
    exchange: Optional[str] = Query(None, description="Exchange ID"),
    type: Optional[str] = Query(None, description="Symbol type")
):
    """Symbol search."""
    try:
        exchange_id = exchange or "binance"  # Default to binance if not specified
        
        # Get symbols from the exchange
        symbols = await ccxt_service.get_symbols(exchange_id.lower())
        
        # Filter by query
        filtered = [
            s for s in symbols
            if query.lower() in s['symbol'].lower() or query.lower() in s['description'].lower()
        ]
        
        # Apply type filter if provided
        if type:
            filtered = [s for s in filtered if s['type'] == type]
            
        # Format results as UDFSearchResult
        results = [
            UDFSearchResult(
                symbol=s['symbol'],
                full_name=s['full_name'],
                description=s['description'],
                exchange=s['exchange'],
                ticker=s['ticker'],
                type=s['type']
            )
            for s in filtered[:limit]
        ]
        
        return results
    except Exception as e:
        print(f"Error in symbol search: {e}")
        return []

@udf_router.get("/symbols")
async def get_symbol_info(symbol: str = Query(..., description="Symbol to get info for")):
    """Symbol resolve."""
    try:
        # Parse the symbol to extract exchange and trading pair
        parts = symbol.split(':')
        if len(parts) == 2:
            exchange_id, pair = parts
        else:
            # Default to binance if not specified
            exchange_id = "binance"
            pair = symbol
            
        # Replace - with / for CCXT compatibility
        pair = pair.replace('-', '/')
        
        exchange = ccxt_service.get_exchange(exchange_id)
        await exchange.load_markets()
        
        if pair not in exchange.markets:
            raise HTTPException(status_code=404, detail=f"Symbol {pair} not found on {exchange_id}")
            
        market = exchange.markets[pair]
        
        return {
            "name": pair,
            "ticker": pair,
            "description": f"{market['base']}/{market['quote']}",
            "type": "crypto",
            "exchange": exchange_id,
            "listed_exchange": exchange_id,
            "timezone": "Etc/UTC",
            "session": "24x7",
            "minmov": 1,
            "pricescale": 10 ** (market.get('precision', {}).get('price', 8)),
            "has_intraday": True,
            "has_daily": True,
            "has_weekly_and_monthly": True,
            "supported_resolutions": ["1", "5", "15", "30", "60", "240", "1D", "1W", "1M"],
            "currency_code": market['quote'],
            "original_currency_code": market['quote'],
            "volume_precision": market.get('precision', {}).get('amount', 8)
        }
        
    except Exception as e:
        print(f"Error in symbol info: {e}")
        return {"s": "error", "errmsg": str(e)}

@udf_router.get("/history")
async def get_history(
    symbol: str = Query(..., description="Symbol"),
    resolution: str = Query(..., description="Resolution"),
    from_time: int = Query(..., alias="from", description="From timestamp"),
    to_time: int = Query(..., alias="to", description="To timestamp")
):
    """Bars history endpoint."""
    try:
        # Parse the symbol to extract exchange and trading pair
        parts = symbol.split(':')
        if len(parts) == 2:
            exchange_id, pair = parts
        else:
            # Default to binance if not specified
            exchange_id = "binance"
            pair = symbol
            
        # Replace - with / for CCXT compatibility
        pair = pair.replace('-', '/')
        
        # Map TradingView resolution to CCXT timeframe
        timeframe = resolution_to_timeframe(resolution)
        
        # Fetch data
        df = await ccxt_service.get_bars(
            exchange_id=exchange_id,
            symbol=pair,
            timeframe=timeframe,
            since=from_time * 1000,  # Convert to milliseconds
            limit=1000  # Adjust as needed
        )
        
        if df.empty:
            return {
                "s": "no_data",
                "nextTime": None
            }
            
        # Format response for UDF
        return {
            "s": "ok",
            "t": [int(ts.timestamp()) for ts in df['timestamp']],
            "o": df['open'].tolist(),
            "h": df['high'].tolist(),
            "l": df['low'].tolist(),
            "c": df['close'].tolist(),
            "v": df['volume'].tolist()
        }
        
    except Exception as e:
        print(f"Error in history data: {e}")
        return {"s": "error", "errmsg": str(e)}