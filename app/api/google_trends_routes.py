from fastapi import APIRouter, HTTPException
from app.services.google_trends_service import GoogleTrendsService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

google_trends_router = APIRouter()
google_trends_service = GoogleTrendsService()

@google_trends_router.get("/historical-google-trends")
async def get_historical_google_trends(search_term: str):
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

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
