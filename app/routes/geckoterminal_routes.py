from fastapi import APIRouter, HTTPException
from app.services.geckoterminal_service import GeckoTerminalService
from app.core.plotly_config import (
    apply_config_to_figure,
    get_chart_colors,
    create_base_layout
)
from app.core.registry import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

geckoterminal_router = APIRouter()
geckoterminal_service = GeckoTerminalService()

AI_AGENT_LIST = {
    "GOAT": {
        "address": "CzLSujWBLFsSjncfkh59rUFqvafWcY5tzedWJSuypump",
        "chain": "solana",
        "pool_id": "9Tb2ohu5P16BpBarqd3N27WnkF51Ukfs8Z1GzzLDxVZW",
    },
    "VIRTUAL": {
        "address": "0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b",
        "chain": "base",
        "pool_id": "0xb909f567c5c2bb1a4271349708cc4637d7318b4a",
    },
    "ZEREBRO": {
        "address": "8x5VqbHA8D7NkD52uNuS5nnt3PwA8pLD34ymskeSo2Wn",
        "chain": "solana",
        "pool_id": "3sjNoCnkkhWPVXYGDtem8rCciHSGc9jSFZuUAzKbvRVp",
    },
    "ACT": {
        "address": "GJAFwWjJ3vnTsrQVabjBVK2TYB1YtRCQXRDfDgUnpump",
        "chain": "solana",
        "pool_id": "B4PHSkL6CeZbxVqm1aUPQuVpc5ERFcaZj7u9dhtphmVX",
    },
    "ANON": {
        "address": "0x0Db510e79909666d6dEc7f5e49370838c16D950f",
        "chain": "base",
        "pool_id": "0xc4ecaf115cbce3985748c58dccfc4722fef8247c",
    },
    "BULLY": {
        "address": "79yTpy8uwmAkrdgZdq6ZSBTvxKsgPrNqTLvYQBh1pump",
        "chain": "solana",
        "pool_id": "A88BtP7EEXYPKgbwvFByMnm5NoM2bKs6s1o1F5u6GohB",
    },
    "FARTCOIN": {
        "address": "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump",
        "chain": "solana",
        "pool_id": "Bzc9NZfMqkXR6fz1DBph7BDf9BroyEf6pnzESP7v5iiw",
    },
    "AI16Z": {
        "address": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
        "chain": "solana",
        "pool_id": "DuYFmgxA4KnXV2Sm754UKw1gZ6B3zksaf4E7ibY4fg9R",
    },
    "CHAOS": {
        "address": "8SgNwESovnbG1oNEaPVhg6CR9mTMSK7jPvcYRe3wpump",
        "chain": "solana",
        "pool_id": "4oxJ9987Jn6J2xMNpg8wusn5MjHQo3SSdJdP9vTrvhmr",
    },
    "PROJECT89": {
        "address": "Bz4MhmVRQENiCou7ZpJ575wpjNFjBjVBSiVhuNg1pump",
        "chain": "solana",
        "pool_id": "2yhXxFHiWjWxMiZMsTPRGhiKTWsuYFFx2us2kH8P7Kpq",
    },
    "AVA": {
        "address": "DKu9kykSfbN5LBfFXtNNDPaX35o4Fv6vJ9FKk7pZpump",
        "chain": "solana",
        "pool_id": "GjvW8JQSpKG5ogjyD3zozfaeJSShTajS5ZFrexT8L12k",
    },
    "MEMESAI": {
        "address": "39qibQxVzemuZTEvjSB7NePhw9WyyHdQCqP8xmBMpump",
        "chain": "solana",
        "pool_id": "6btaEBWeGTucPsuXrSBmbdmqdR6S7MaBV4RkzbipHEYu",
    },
    "AVB": {
        "address": "6d5zHW5B8RkGKd51Lpb9RqFQSqDudr9GJgZ1SgQZpump",
        "chain": "solana",
        "pool_id": "BVSiP9RR4T8ZqY4ZLkgsxNwKZoEVbB92RsWN5tCdtRox",
    },
    "AIXBT": {
        "address": "0x4F9Fd6Be4a90f2620860d680c0d4d5Fb53d1A825",
        "chain": "base",
        "pool_id": "0x7464850cc1cfb54a2223229b77b1bca2f888d946",
    },
    "LUNA": {
        "address": "0x55cD6469F597452B5A7536e2CD98fDE4c1247ee4",
        "chain": "base",
        "pool_id": "0xa8e64fb120ce8796594670bae72279c8aa1e5359",
    },
    "LOLA": {
        "address": "AKyVUXwrYPxnt9cf9EQUpRmty6yrW25d3R8R1YVepump",
        "chain": "solana",
        "pool_id": "Bm99GtoXnnY3Z17BqVo3Yqx6X2k45jrwiy7k4ceGgpFs",
    },
    "ELIZA": {
        "address": "5voS9evDjxF589WuEub5i4ti7FWQmZCsAsyD5ucbuRqM",
        "chain": "solana",
        "pool_id": "U71hPHrnG3mNJzTHyK1rmuNzySs97pnoGbwX3t5xeyx",
    },
    "FATHA": {
        "address": "EWWDzCwq4UYW3ERTXbdgd6X6sdkKHFMJqRz1ZiFcpump",
        "chain": "solana",
        "pool_id": "Am1SqWAHhaKWS4H9uwHweeYxCaECR5yDYZiX1jD9RVMP",
    },
    "OPAIUM": {
        "address": "EWWDzCwq4UYW3ERTXbdgd6X6sdkKHFMJqRz1ZiFcpump",
        "chain": "solana",
        "pool_id": "Am1SqWAHhaKWS4H9uwHweeYxCaECR5yDYZiX1jD9RVMP",
    },
    "PIPPIN": {
        "address": "Dfh5DzRgSvvCFDoYc2ciTkMrbDfRKybA4SoFbPmApump",
        "chain": "solana",
        "pool_id": "8WwcNqdZjCY5Pt7AkhupAFknV2txca9sq6YBkGzLbvdt",
    },
    "NEROBOSS": {
        "address": "5HTp1ebDeBcuRaP4J6cG3r4AffbP4dtcrsS7YYT7pump",
        "chain": "solana",
        "pool_id": "BCPMP9QSQtVWe9iaDUxvZyf2jcgghYtnryb3s9WkJKtr",
    },
    "FLOWER": {
        "address": "AVyjco9j8vv7ZPkhCpEoPJ3bLEuw7G1wrrNt8DrApump",
        "chain": "solana",
        "pool_id": "DgwxYGU4ucQCiw8o2HjxwDH3PE5nSQWafHCYwaPtRVyN",
    },
    "GNON": {
        "address": "HeJUFDxfJSzYFUuHLxkMqCgytU31G6mjP4wKviwqpump",
        "chain": "solana",
        "pool_id": "2ur2GZKShAp8xJ33QSs7C5ZUTD9mRjVrgwoHR2Q7T1Sv",
    },
    "OPUS": {
        "address": "9JhFqCA21MoAXs2PTaeqNQp2XngPn1PgYr2rsEVCpump",
        "chain": "solana",
        "pool_id": "HrYPN3eAQA26JSBF9DUFwztTR35Cef7dAg93BA8ikn3M",
    },
    "REX": {
        "address": "CNKEXXypBC66cZ111Mg3JUxyczXS1E9T6MWEufzQZVMo",
        "chain": "solana",
        "pool_id": "9cLdqfgZJFAi91Uq4bQMHSWrtfKgwPfvcEcUjrH2tPKB",
    },
    "AIKO": {
        "address": "mdx5dxD754H8uGrz6Wc96tZfFjPqSgBvqUDbKycpump",
        "chain": "solana",
        "pool_id": "8UqSQJmssioVD8vDutcidnTSj2VzRbLEnAMbLvgMBxqq",
    },
    "VADER": {
        "address": "0x731814e491571A2e9eE3c5b1F7f3b962eE8f4870",
        "chain": "base",
        "pool_id": "0xa1dddb82501e8fe2d92ad0e8ba331313f501de72",
    },
    "VVAIFU": {
        "address": "FQ1tyso61AH1tzodyJfSwmzsD3GToybbRNoZxUBz21p8",
        "chain": "solana",
        "pool_id": "9UMuN94bbuH53F4PTVWDYZoQjsJ3zgEx2j2vtT5Rbo1x",
    },
}

@geckoterminal_router.get("/ai-agents-market-data")
@register_widget({
    "name": "AI Agents Market Data",
    "description": "Market data for AI agent tokens",
    "category": "crypto",
    "endpoint": "geckoterminal/ai-agents-market-data",
    "gridData": {"w": 20, "h": 9},
    "source": "GeckoTerminal",
    "type": "table",
    "data": {
        "table": {
            "showAll": True,
            "columnsDefs": [
                {
                    "headerName": "Name",
                    "field": "name",
                    "chartDataType": "category",
                },
                {
                    "headerName": "Symbol",
                    "field": "symbol",
                    "chartDataType": "category",
                },
                {
                    "headerName": "Price",
                    "field": "price_usd",
                    "chartDataType": "series",
                },
                {
                    "headerName": "Volume",
                    "field": "volume_usd",
                    "chartDataType": "series",
                },
                {
                    "headerName": "Market Cap",
                    "field": "market_cap_usd",
                    "chartDataType": "series",
                },
            ],
        }
    },
})
async def get_ai_agents_market_data():
    try:
        data = await geckoterminal_service.fetch_ai_agent_market_data(AI_AGENT_LIST)
        data.fillna(0, inplace=True)

        float_columns = ['price_usd', 'volume_usd', 'market_cap_usd', 'fdv_usd', 
                        'total_supply', 'total_reserve_in_usd']
        for col in float_columns:
            if col in data.columns:
                data[col] = data[col].astype(float, errors='ignore')
                
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@geckoterminal_router.get("/candles")
@register_widget({
    "name": "GeckoTerminal Candles",
    "description": "OHLCV data for a given pool from GeckoTerminal",
    "category": "crypto",
    "type": "chart",
    "endpoint": "geckoterminal/candles",
    "gridData": {"w": 20, "h": 9},
    "source": "GeckoTerminal",
    "params": [
        {
            "paramName": "chain",
            "value": "solana",
            "label": "Chain",
            "type": "text",
            "description": "Chain (e.g. solana)",
        },
        {
            "paramName": "pool_id",
            "value": "2cWGVhRAo7SF6BtaNuivDSPCncGnEfLWwMPrKk5ikeXk",
            "label": "Pool ID",
            "type": "text",
            "description": "Pool ID",
        },
        {
            "paramName": "timeframe",
            "value": "minute",
            "label": "Timeframe",
            "type": "text",
            "description": "Timeframe (e.g. minute, hour, day)",
            "options": [{"label": "Minute", "value": "minute"}, {"label": "Hour", "value": "hour"}, {"label": "Day", "value": "day"}]
        },
        {
            "paramName": "aggregate",
            "value": "1",
            "label": "Aggregate",
            "type": "text",
            "description": "Number of periods to aggregate",
        },
    ],
    "data": {"chart": {"type": "candlestick"}},
})
async def get_geckoterminal_candles(
    pool_id: str,
    chain: str,
    timeframe: str, 
    aggregate: int, 
    theme: str = "dark"
):
    try:
        data = await geckoterminal_service.fetch_pool_ohlcv_data(
            pool_id, chain, timeframe, aggregate
        )
        data["timestamp"] = pd.to_datetime(data["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        # Define theme-specific colors
        increasing_color = colors.get('positive', '#26a69a')
        decreasing_color = colors.get('negative', '#ef5350')
        # Semi-transparent gray for volume
        volume_color = 'rgba(128,128,128,0.5)'
        zero_line_color = colors.get('neutral', 'lightgrey')
        
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                y_dtype="$,.4f",
                theme=theme
            )
        )

        # Add volume bars on secondary y-axis with theme-appropriate color
        figure.add_bar(
            x=data.index,
            y=data['volume'],
            name="Volume",
            yaxis="y2",
            marker_color=volume_color
        )

        # Add candlestick chart with theme-appropriate colors
        figure.add_candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name="Price",
            increasing_line_color=increasing_color,
            decreasing_line_color=decreasing_color
        )

        # Update layout to include secondary y-axis for volume
        # Use theme-appropriate colors for grid and zero lines
        figure.update_layout(
            yaxis=dict(
                rangemode="nonnegative",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor=zero_line_color
            ),
            yaxis2=dict(
                title="Volume",
                overlaying="y", 
                side="right",
                showgrid=False,
                rangemode="nonnegative",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor=zero_line_color
            ),
        )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
  
