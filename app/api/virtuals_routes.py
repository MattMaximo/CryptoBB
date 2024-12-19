from fastapi import APIRouter, HTTPException
from app.services.virtuals_service import VirtualsService

virtuals_router = APIRouter()
virtuals_service = VirtualsService()

@virtuals_router.get("/agents-data")
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