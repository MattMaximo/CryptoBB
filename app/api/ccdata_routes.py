from fastapi import APIRouter, HTTPException
from app.services.ccdata_service import CCDataService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
from app.core.widget_decorator import register_widget
import plotly.graph_objects as go
import pandas as pd
from typing import List
import json
import asyncio

ccdata_router = APIRouter()
ccdata_service = CCDataService()
   
@ccdata_router.get("/exchange-price-deltas")
@register_widget({
    "name": "Exchange Price Deltas",
    "description": (
        "This is the percent difference between the vwap price of BTC on each "
        "exchange and the average price of BTC across those exchanges."
    ),
    "category": "crypto",
    "defaultViz": "chart",
    "endpoint": "ccdata/exchange-price-deltas",
    "widgetId": "ccdata/exchange-price-deltas",
    "gridData": {"w": 20, "h": 9},
    "source": "CCData",
    "data": {"chart": {"type": "line"}},
})
async def get_exchange_price_deltas(theme: str = "dark"):
    try:
        data = await ccdata_service.get_delta_data()
        data['timestamp'] = data['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Delta",
                y_dtype=".2%",
                theme=theme
            )
        )

        # Add delta lines on primary y-axis
        for col in data.columns:
            if col != 'average_price':
                fig.add_scatter(
                    x=data.index,
                    y=data[col],
                    mode="lines", 
                    name=col.split('_')[0],
                    hovertemplate="%{y:.3%}"
                )

        fig.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y", 
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            )
        )
        # Add average price line on secondary y-axis
        fig.add_scatter(
            x=data.index,
            y=data['average_price'],
            mode="lines",
            name="Average Price",
            line=dict(color=colors['sma_line'], width=1),
            yaxis="y2",
            hovertemplate="%{y:,.2f}",
        )

        # Apply the standard configuration to the figure with theme
        fig, config = apply_config_to_figure(fig, theme=theme)

        # Convert figure to JSON with the config
        figure_json = fig.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@ccdata_router.get("/candles")
@register_widget({
    "name": "CCData Candles",
    "description": "OHLCV data for a given pool",
    "category": "crypto",
    "defaultViz": "chart",
    "endpoint": "ccdata/candles",
    "widgetId": "ccdata/candles",
    "gridData": {"w": 20, "h": 9},
    "source": "CCData",
    "params": [
        {
            "paramName": "exchange",
            "value": "binance",
            "label": "Exchange",
            "type": "text",
            "description": "Exchange to fetch data from (e.g. binance, kraken, mexc)",
        },
        {
            "paramName": "symbol",
            "value": "BTC-USDT",
            "label": "Pair",
            "type": "text",
            "description": "Pair (e.g. BTC-USDT) to fetch data for",
        },
        {
            "paramName": "interval",
            "value": "hours",
            "label": "Interval",
            "type": "text",
            "description": "Interval to fetch data for (options: minutes, hours, days)",
        },
        {
            "paramName": "aggregate",
            "value": "1",
            "label": "Aggregate",
            "type": "text",
            "description": "Aggregation interval. Options: day = [1], hour = [1, 4, 12], minute = [1, 5, 15]",
        },
    ],
    "data": {"chart": {"type": "candlestick"}},
})
async def get_ccdata_candles(
    exchange: str, 
    symbol: str, 
    interval: str, 
    aggregate: int, 
    theme: str = "dark"
):
    try:
        data = await ccdata_service._fetch_spot_data(
            (exchange, symbol), 
            interval=interval, 
            aggregate=aggregate, 
            limit=2000
        )
        data = pd.DataFrame(data)
        data = data[['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]
        data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], unit='s')
        if interval == "minutes" or interval == "hours":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d %H:%M:%S")
        elif interval == "day":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d")
        data = data.set_index("TIMESTAMP")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                y_dtype="$,.4f",
                theme=theme
            )
        )
        # Add volume bars on secondary y-axis first so they appear behind candlesticks
        figure.add_bar(
            x=data.index,
            y=data['VOLUME'],
            name="Volume",
            yaxis="y2",
            marker_color='rgba(128,128,128,0.5)'
        )
        # Add candlestick chart second so it appears on top
        figure.add_candlestick(
            x=data.index,
            open=data['OPEN'],
            high=data['HIGH'],
            low=data['LOW'],
            close=data['CLOSE'],
            name="Price",
            increasing_line_color=colors['positive'],
            decreasing_line_color=colors['negative']
        )
        # Update layout to include secondary y-axis for volume
        figure.update_layout(
            yaxis=dict(
                rangemode="nonnegative",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey"
            ),
            yaxis2=dict(
                title="Volume",
                overlaying="y", 
                side="right",
                showgrid=False,
                rangemode="nonnegative",
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="lightgrey"
            ),
        )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@ccdata_router.get("/exchange-spot-volume")
@register_widget({
    "name": "Total Spot Exchange Volume",
    "description": "Total spot volume for a given exchange.",
    "category": "crypto",
    "endpoint": "ccdata/exchange-spot-volume",
    "widgetId": "ccdata/exchange-spot-volume",
    "gridData": {"w": 20, "h": 9},
    "params": [
        {
            "paramName": "exchange",
            "value": "binance",
            "label": "Exchange",
        }
    ],
    "source": "CCData",
    "defaultViz": "chart",
    "data": {"chart": {"type": "line"}},
})
async def get_exchange_data(exchange: str, theme: str = "dark"):
    try:
        # First get all instruments for the exchange
        data = await ccdata_service.get_total_exchange_volume(exchange)
        data['timestamp'] = data['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Volume",
                y_dtype=",.2f",
                theme=theme
            )
        )

        fig.add_scatter(
            x=data.index,
            y=data['total_volume'],
            mode="lines",
            name="Total Volume",
            line=dict(color=colors['main_line']),
            hovertemplate="%{y:,.2f}"
        )

        # Apply the standard configuration to the figure with theme
        fig, config = apply_config_to_figure(fig, theme=theme)

        # Convert figure to JSON with the config
        figure_json = fig.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

