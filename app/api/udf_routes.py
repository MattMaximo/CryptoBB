from fastapi import APIRouter, Query
from typing import Optional
from app.services.velo_service import UDFService

router = APIRouter()
udf_service = UDFService()

@router.get("/config")
async def config():
    return udf_service.get_config()

@router.get("/symbols")
async def symbols(symbol: str):
    return udf_service.get_symbol_info(symbol)

@router.get("/history")
async def history(
    symbol: str,
    from_: Optional[int] = Query(None, alias="from"),
    to: Optional[int] = None,
    resolution: Optional[str] = None
):
    return udf_service.get_history(symbol, from_, to, resolution)

@router.get("/time")
async def time():
    return udf_service.get_time()

@router.get("/search")
async def search(
    query: str,
    limit: Optional[int] = 30,
    type: Optional[str] = None,
    exchange: Optional[str] = None
):
    return udf_service.search_symbols(query, limit)