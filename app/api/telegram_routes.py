from fastapi import APIRouter, HTTPException
from app.services.telegram_service import TelegramService
from app.assets.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

telegram_router = APIRouter()
telegram_service = TelegramService()

@telegram_router.get("/coinbase_app_store_rank")
async def get_coinbase_app_store_rank_route():
    try:
        data = await telegram_service.get_coinbase_app_store_rank()

        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#034AF6")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@telegram_router.get("/coinbase_wallet_app_store_rank")
async def get_coinbase_wallet_app_store_rank_route():
    try:
        data = await telegram_service.get_coinbase_wallet_app_store_rank()
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#82a7ff")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@telegram_router.get("/phantom_wallet_app_store_rank")
async def get_phantom_wallet_app_store_rank_route():
    try:
        data = await telegram_service.get_phantom_wallet_app_store_rank()
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#9382DE")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

