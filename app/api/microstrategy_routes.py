from fastapi import APIRouter, HTTPException
from app.services.microstrategy_service import MicrostrategyService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

microstrategy_router = APIRouter()
microstrategy_service = MicrostrategyService()

@microstrategy_router.get("/premium")
async def get_microstrategy_premium():
    try:
        data = await microstrategy_service.get_prices()
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Nav Premium"
            )
        )

        # Add secondary Y axis for price
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y", 
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["nav_premium"],
            mode="lines",
            name="NAV Premium",
            line=dict(color="#D8232E"),
            hovertemplate="%{y:.2f}"
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["btc_price"],
            mode="lines", 
            name="BTC Price",
            line=dict(color="#F7931A"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@microstrategy_router.get("/info")
async def get_microstrategy_info():
    try:
        data = await microstrategy_service.get_treasury_data()
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  