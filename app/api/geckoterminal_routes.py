from fastapi import APIRouter, HTTPException
from app.services.geckoterminal_service import GeckoTerminalService
from app.assets.base_chart_layout import create_base_layout
from app.assets.ai_agent_mapping import ai_agent_mapping
import plotly.graph_objects as go
import pandas as pd
import json

geckoterminal_router = APIRouter()
geckoterminal_service = GeckoTerminalService()

@geckoterminal_router.get("/ai_agents_market_data")
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
async def get_geckoterminal_candles(symbol: str, timeframe: str, aggregate: int):
    try:
        pool_id = ai_agent_mapping[symbol.upper()]['pool_id']
        chain = ai_agent_mapping[symbol.upper()]['chain']
        data = await geckoterminal_service.fetch_pool_ohlcv_data(pool_id, chain, timeframe, aggregate)
        data["timestamp"] = pd.to_datetime(data["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        data = data.set_index("timestamp")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                y_dtype="$,.4f"
            )
        )

        # Add volume bars on secondary y-axis
        figure.add_bar(
            x=data.index,
            y=data['volume'],
            name="Volume",
            yaxis="y2",
            marker_color='rgba(128,128,128,0.5)'
        )

        # Add candlestick chart
        figure.add_candlestick(
            x=data.index,
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
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
  
