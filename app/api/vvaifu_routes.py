from fastapi import APIRouter, HTTPException
from app.services.vvaifu_service import VVaifuService

vvaifu_router = APIRouter()
vvaifu_service = VVaifuService()

@vvaifu_router.get("/agents-data")
async def get_agents_list():
    """Get list of all VVaifu agents with their market data"""
    try:
        data = await vvaifu_service.fetch_all_data()
        data.fillna(0, inplace=True)
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 