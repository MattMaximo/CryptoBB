from fastapi import APIRouter, HTTPException
from app.services.virtuals_service import VirtualsService
from app.core.registry import register_widget

virtuals_router = APIRouter()
virtuals_service = VirtualsService()

@virtuals_router.get("/agents-data")
@register_widget({
    "name": "Virtuals Agents List",
    "description": "List of virtual agents and their data",
    "category": "crypto",
    "endpoint": "virtuals/agents-data",
    "gridData": {"w": 20, "h": 9},
    "source": "Virtuals Protocol",
})
async def get_agents_list():
    """
    Get list of virtual agents and their data
    """
    try:
        df = await virtuals_service.get_agents_list()
        df.fillna(0, inplace=True)
        return df.to_dict(orient="records") 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))