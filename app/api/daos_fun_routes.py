from fastapi import APIRouter, HTTPException
from app.services.daos_fun_service import DaosFunService

daos_fun_router = APIRouter()
daos_fun_service = DaosFunService()

@daos_fun_router.get("/daos-data")
async def get_daos():
    try:
        data = await daos_fun_service.get_dao_data()
        data = data[['dao_name', 'twitter_handle', 'twitter_url', 'market_cap', 
                    'market_cap_change', 'volume', 'treasury', 'treasury_change', 
                    'multiplier']]
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 