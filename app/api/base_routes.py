from fastapi import APIRouter, HTTPException
from app.core.widgets import WIDGETS

base_router = APIRouter()

@base_router.get("/widgets.json")
async def get_widgets():
    return WIDGETS
