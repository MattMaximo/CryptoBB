from fastapi import APIRouter
from app.core.templates import TEMPLATES
from app.core.widget_decorator import register_widget, WIDGETS

base_router = APIRouter()

@base_router.get("/widgets.json")
async def get_widgets():
    return WIDGETS

@base_router.get("/templates.json")
@register_widget({
    "name": "Templates JSON",
    "description": "List of all available dashboard templates in the system",
    "category": "system",
    "endpoint": "templates.json",
    "isUtility": True,
})
async def get_templates():
    return TEMPLATES
