from fastapi import APIRouter, HTTPException
from app.services.microstrategy_service import MicrostrategyService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
from app.core.widget_decorator import register_widget
import plotly.graph_objects as go
import pandas as pd
import json


microstrategy_router = APIRouter()

microstrategy_service = MicrostrategyService()


@microstrategy_router.get("/premium")
@register_widget({
    "name": "Microstrategy Premium",
    "description": (
        "Premium/discount of Microstrategy's stock price relative to "
        "its Bitcoin holdings"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "microstrategy/premium",
    "gridData": {"w": 20, "h": 9},
    "source": "Microstrategy",
    "data": {"chart": {"type": "line"}},
})
async def get_microstrategy_premium(theme: str = "dark"):
    try:
        data = await microstrategy_service.get_prices()
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Nav Premium",
                theme=theme
            )
        )

        # Add secondary Y axis for price
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y", 
                side="right",
                gridcolor="#2f3338" if theme == "dark" else "#dddddd",
                color=colors['text']
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["nav_premium"],
            mode="lines",
            name="NAV Premium",
            line=dict(color=colors['negative']),
            hovertemplate="%{y:.2f}"
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["btc_price"],
            mode="lines", 
            name="BTC Price",
            line=dict(color=colors['main_line']),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@microstrategy_router.get("/info")
@register_widget({
    "name": "Microstrategy Info",
    "description": (
        "Historical info for Microstrategy's Bitcoin holdings, including "
        "balance, cost basis, and share metrics"
    ),
    "category": "crypto",
    "type": "table",
    "endpoint": "microstrategy/info",
    "gridData": {"w": 20, "h": 9},
    "source": "Microstrategy",
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {
                    "headerName": "Date",
                    "field": "date",
                    "chartDataType": "category",
                },
                {
                    "headerName": "BTC Balance",
                    "field": "btc_balance",
                    "chartDataType": "series",
                },
                {
                    "headerName": "Cost Basis",
                    "field": "cost_basis",
                    "chartDataType": "series",
                },
                {
                    "headerName": "BTC per Share",
                    "field": "btc_per_share",
                    "chartDataType": "series",
                },
            ],
        }
    },
})
async def get_microstrategy_info():
    try:
        data = await microstrategy_service.get_treasury_data()
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  