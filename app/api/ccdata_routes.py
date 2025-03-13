from fastapi import APIRouter, HTTPException
from app.services.ccdata_service import CCDataService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
from typing import List
import json
import asyncio

ccdata_router = APIRouter()
ccdata_service = CCDataService()
   
@ccdata_router.get("/exchange-price-deltas")
async def get_exchange_price_deltas():
    try:
        data = await ccdata_service.get_delta_data()
        data['timestamp'] = data['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Delta",
                y_dtype=".2%"
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
            line=dict(color="white", width=1),
            yaxis="y2",
            hovertemplate="%{y:,.2f}",
        )

        return json.loads(fig.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@ccdata_router.get("/candles")
async def get_ccdata_candles(exchange: str, symbol: str, interval: str, aggregate: int):

    try:
        data = await ccdata_service._fetch_spot_data((exchange, symbol), interval=interval, aggregate=aggregate, limit=2000)
        data = pd.DataFrame(data)
        data = data[['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]
        data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], unit='s')
        if interval == "minutes" or interval == "hours":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d %H:%M:%S")
        elif interval == "day":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d")
        data = data.set_index("TIMESTAMP")
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                y_dtype="$,.4f"
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
            name="Price"
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
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    




@ccdata_router.get("/exchange-spot-volume")
async def get_exchange_data(exchange: str):
    try:
        # First get all instruments for the exchange
        data = await ccdata_service.get_total_exchange_volume(exchange)
        data['timestamp'] = data['timestamp'].dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Volume",
                y_dtype=".2s"
            )
        )

        fig.add_scatter(
            x=data.index,
            y=data['total_volume'],
            mode="lines",
            name="Total Volume",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(fig.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

