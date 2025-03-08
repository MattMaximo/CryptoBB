from fastapi import APIRouter, HTTPException
from app.core.widgets import WIDGETS
from app.core.templates import TEMPLATES

base_router = APIRouter()

@base_router.get("/widgets.json")
async def get_widgets():
    return WIDGETS

@base_router.get("/templates.json")
async def get_templates():
    return TEMPLATES
