from fastapi import APIRouter, HTTPException
from app.services.aave_service import AaveService
from app.core.plotly_config import (
    apply_config_to_figure,
    get_chart_colors,
    create_base_layout
)
from app.core.registry import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

aave_router = APIRouter()
aave_service = AaveService()

AAVE_POOLS = [
    {
        "Pool Address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc20x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "WETH",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca00x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "wstETH",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "weETH",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c5990x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "WBTC",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x2260fac5e5542a773aa44fbcfedf7c193bc2c599&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0xdac17f958d2ee523a2206206994597c13d831ec70x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "USDT",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xdac17f958d2ee523a2206206994597c13d831ec7&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "USDC",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
        "Pool Name": "cbBTC",
        "Chain": "Ethereum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf&marketName=proto_mainnet_v3"
    },
    {
        "Pool Address": "0x42000000000000000000000000000000000000060xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "WETH",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x4200000000000000000000000000000000000006&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0x04c0599ae5a44757c0af6f9ec3b93da8976c150a0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "weETH",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x04c0599ae5a44757c0af6f9ec3b93da8976c150a&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0x833589fcd6edb6e08f4c7c32d4f71b54bda029130xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "USDC",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x833589fcd6edb6e08f4c7c32d4f71b54bda02913&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "cbBTC",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0xc1cba3fcea344f92d9239c08c0568f6f2f0ee4520xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "wstETH",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xc1cba3fcea344f92d9239c08c0568f6f2f0ee452&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec220xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D8453",
        "Pool Name": "cbETH",
        "Chain": "Base",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec22&marketName=proto_base_v3"
    },
    {
        "Pool Address": "0x82af49447d8a07e3bd95bd0d56f35241523fbab10xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "WETH",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x82af49447d8a07e3bd95bd0d56f35241523fbab1&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "WBTC",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0x35751007a407ca6feffe80b3cb397736d2cf4dbe0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "weETH",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x35751007a407ca6feffe80b3cb397736d2cf4dbe&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0xaf88d065e77c8cc2239327c5edb3a432268e58310xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "USDC",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xaf88d065e77c8cc2239327c5edb3a432268e5831&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0x5979d7b546e38e414f7e9822514be443a48005290xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "wstETH",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x5979d7b546e38e414f7e9822514be443a4800529&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb90xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "USDT",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0x912ce59144191c1204e64559fe8253a0e49e65480xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "ARB",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0x912ce59144191c1204e64559fe8253a0e49e6548&marketName=proto_arbitrum_v3"
    },
    {
        "Pool Address": "0xf97f4df75117a78c1a5a0dbb814af92458539fb40xa97684ead0e402dC232d5A977953DF7ECBaB3CDb42161",
        "Pool Name": "LINK",
        "Chain": "Arbitrum",
        "Version": "v3",
        "Link": "https://app.aave.com/reserve-overview/?underlyingAsset=0xf97f4df75117a78c1a5a0dbb814af92458539fb4&marketName=proto_arbitrum_v3"
    }
]

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
    "type": "chart",
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
    "type": "chart",
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
    "type": "chart",
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