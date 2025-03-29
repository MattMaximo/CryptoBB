from fastapi import APIRouter, HTTPException
from app.services.google_trends_service import GoogleTrendsService
from app.core.registry import register_widget
from app.core.plotly_config import create_base_layout, apply_config_to_figure
import plotly.graph_objects as go
import pandas as pd
import json

google_trends_router = APIRouter()
google_trends_service = GoogleTrendsService()

@google_trends_router.get("/historical-google-trends")
@register_widget({
    "name": "Historical Google Trends",
    "description": "Historical Google Trends for a given search term",
    "category": "google",
    "endpoint": "google-trends/historical-google-trends",
    "gridData": {"w": 20, "h": 9},
    "source": "Google Trends",
    "type": "chart",
    "params": [
        {
            "paramName": "search_term",
            "value": "bitcoin",
            "label": "Search Term",
        }
    ],
})
async def get_historical_google_trends(search_term: str, theme: str = "dark"):
    try:
        data = google_trends_service.get_historical_search_trends(search_term)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Search Interest"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data[search_term],
            mode="lines",
            line=dict(color="#E3BF1E")
        )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
