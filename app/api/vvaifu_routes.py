from fastapi import APIRouter, HTTPException
from app.services.vvaifu_service import VVaifuService
from app.core.registry import register_widget

vvaifu_router = APIRouter()
vvaifu_service = VVaifuService()

@vvaifu_router.get("/agents-data")
@register_widget({
    "name": "VVaifu Agents List",
    "description": "List of VVaifu agents with their market data",
    "category": "crypto",
    "endpoint": "vvaifu/agents-data",
    "gridData": {"w": 20, "h": 9},
    "source": "VVaifu"
})
async def get_agents_list():
    try:
        data = await vvaifu_service.fetch_all_data()
        data.fillna(0, inplace=True)
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 