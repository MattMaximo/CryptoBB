from fastapi import APIRouter, HTTPException
from app.services.geckoterminal_service import GeckoTerminalService
from app.core.plotly_config import (
    apply_config_to_figure,
    get_chart_colors,
    create_base_layout
)
from app.assets.ai_agent_mapping import ai_agent_mapping
from app.core.registry import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

geckoterminal_router = APIRouter()
geckoterminal_service = GeckoTerminalService()

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
        data = await geckoterminal_service.fetch_ai_agent_market_data(ai_agent_mapping)
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
  
