from fastapi import APIRouter, HTTPException
from app.core.widgets import WIDGETS

general_router = APIRouter()

@general_router.get("/widgets.json")
async def get_widgets():
    return WIDGETS
