from fastapi import APIRouter, HTTPException
from app.services.aave_service import AaveService
from app.assets.base_chart_layout import create_base_layout
from app.assets.aave_pools import AAVE_POOLS
import plotly.graph_objects as go
import pandas as pd
import json

aave_router = APIRouter()
aave_service = AaveService()



@aave_router.get("/lending_rate")
async def get_aave_lending_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"liquidityRate_avg": "lending_rate"}, inplace=True)
        data = data[["date", "lending_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Lending Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lending_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/utilization_rate")
async def get_aave_utilization_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"utilizationRate_avg": "utilization_rate"}, inplace=True)
        data = data[["date", "utilization_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Utilization Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["utilization_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/borrow_rate")
async def get_aave_borrow_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"variableBorrowRate_avg": "borrow_rate"}, inplace=True)
        data = data[["date", "borrow_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Borrow Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["borrow_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/pools")
async def get_aave_pools():
    return AAVE_POOLS