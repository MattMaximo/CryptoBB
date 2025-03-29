from fastapi import APIRouter, HTTPException
from app.services.aave_service import AaveService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.aave_pools import AAVE_POOLS
from app.assets.charts.plotly_config import (
    apply_config_to_figure,
    get_chart_colors
)
from app.core.widget_decorator import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

aave_router = APIRouter()
aave_service = AaveService()

# Default pool (USDC on Ethereum)
DEFAULT_POOL = (
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"
)


@aave_router.get("/lending-rate")
@register_widget({
    "name": "AAVE Lending Rate",
    "description": "Historical lending rate for AAVE pools",
    "category": "defi",
    "defaultViz": "chart",
    "endpoint": "aave/lending-rate",
    "gridData": {"w": 20, "h": 9},
    "source": "AAVE",
    "params": [
        {
            "paramName": "pool",
            "value": DEFAULT_POOL,
            "label": "Pool",
            "show": True,
            "type": "endpoint",
            "optionsEndpoint": "aave/pools-formatted",
            "description": "AAVE pool address",
            "style": {"popupWidth": 600},
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_aave_lending_rate(
    pool: str = DEFAULT_POOL,
    theme: str = "dark"
):
    try:
        data = await aave_service.get_lending_pool_history(pool)
        data.rename(columns={"liquidityRate_avg": "lending_rate"}, inplace=True)
        data = data[["date", "lending_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Lending Rate",
                y_dtype=".2%",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lending_rate"],
            mode="lines",
            line=dict(color=colors["main_line"])
        )

        # Apply the configuration to the figure
        figure = apply_config_to_figure(figure, theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/utilization-rate")
@register_widget({
    "name": "AAVE Utilization Rate",
    "description": "Historical utilization rate for AAVE pools",
    "category": "defi",
    "defaultViz": "chart",
    "endpoint": "aave/utilization-rate",
    "gridData": {"w": 40, "h": 13},
    "source": "AAVE",
    "params": [
        {
            "paramName": "pool",
            "value": DEFAULT_POOL,
            "label": "Pool",
            "show": True,
            "type": "endpoint",
            "optionsEndpoint": "aave/pools-formatted",
            "description": "AAVE pool address",
            "style": {"popupWidth": 600},
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_aave_utilization_rate(
    pool: str = DEFAULT_POOL,
    theme: str = "dark"
):
    try:
        data = await aave_service.get_lending_pool_history(pool)
        data.rename(columns={"utilizationRate_avg": "utilization_rate"}, inplace=True)
        data = data[["date", "utilization_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Utilization Rate",
                y_dtype=".2%",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["utilization_rate"],
            mode="lines",
            line=dict(color=colors["main_line"])
        )

        # Apply the configuration to the figure
        figure = apply_config_to_figure(figure, theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/borrow-rate")
@register_widget({
    "name": "AAVE Borrow Rate",
    "description": "Historical borrow rate for AAVE pools",
    "category": "defi",
    "defaultViz": "chart",
    "endpoint": "aave/borrow-rate",
    "gridData": {"w": 20, "h": 9},
    "source": "AAVE",
    "params": [
        {
            "paramName": "pool",
            "value": DEFAULT_POOL,
            "label": "Pool",
            "show": True,
            "type": "endpoint",
            "optionsEndpoint": "aave/pools-formatted",
            "description": "AAVE pool address",
            "style": {"popupWidth": 600},
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_aave_borrow_rate(
    pool: str = DEFAULT_POOL,
    theme: str = "dark"
):
    try:
        data = await aave_service.get_lending_pool_history(pool)
        data.rename(columns={"variableBorrowRate_avg": "borrow_rate"}, inplace=True)
        data = data[["date", "borrow_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Borrow Rate",
                y_dtype=".2%",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["borrow_rate"],
            mode="lines",
            line=dict(color=colors["main_line"])
        )

        # Apply the configuration to the figure
        figure = apply_config_to_figure(figure, theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@aave_router.get("/pools")
@register_widget({
    "name": "AAVE Pools",
    "description": "List of all available AAVE pools",
    "category": "defi",
    "endpoint": "aave/pools",
    "isUtility": True,
    "source": "AAVE",
})
async def get_aave_pools():
    return AAVE_POOLS


@aave_router.get("/pools-formatted")
@register_widget({
    "name": "AAVE Pools Formatted",
    "description": "Formatted list of AAVE pools for dropdown selection",
    "category": "defi",
    "endpoint": "aave/pools-formatted",
    "isUtility": True,
    "source": "AAVE",
})
async def get_aave_pools_formatted():
    """
    Returns a formatted list of Aave pools in the format:
    {
        "value": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "label": "USDC (Ethereum)",
        "extraInfo": {
            "description": "USDC on Ethereum (v3)",
            "chain": "Ethereum",
            "version": "v3",
            "link": "https://app.aave.com/..."
        }
    }
    """
    formatted_pools = []
    for pool in AAVE_POOLS:
        pool_address = pool["Pool Address"]
        pool_name = pool["Pool Name"]
        chain = pool["Chain"]
        version = pool["Version"]
        
        formatted_pools.append({
            "value": pool_address,
            "label": f"{pool_name} ({chain})",
            "extraInfo": {
                "description": (
                    f"{pool_name} on {chain} ({version})"
                )
            }
        })
    return formatted_pools