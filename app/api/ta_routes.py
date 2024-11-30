from fastapi import APIRouter, HTTPException
from app.services.ccdata_service import CCDataService
from app.assets.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

ta_router = APIRouter()

ccdata_service = CCDataService()

@ta_router.get("/rsi")
async def get_rsi(exchange: str, symbol: str, interval: str, aggregate: int):
    try:
        data = ccdata_service._fetch_spot_data((exchange, symbol), interval=interval, aggregate=aggregate, limit=2000)
        data = pd.DataFrame(data)
        data = data[['TIMESTAMP', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]
        data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], unit='s')
        if interval == "minutes" or interval == "hours":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d %H:%M:%S")
        elif interval == "day":
            data['TIMESTAMP'] = data['TIMESTAMP'].dt.strftime("%Y-%m-%d")
        data = data.set_index("TIMESTAMP")

        # Calculate RSI
        delta = data['CLOSE'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Calculate 3-period MA of RSI
        data['RSI_MA3'] = data['RSI'].rolling(window=3).mean()

        # Create the chart with modified layout
        layout = create_base_layout(x_title="Date", y_title="RSI", y_dtype="d")
        layout.update(
            yaxis=dict(
                range=[0, 100],
                showgrid=False,
                dtick=10
            ),
            xaxis=dict(
                showgrid=False
            )
        )

        fig = go.Figure(layout=layout)
        
        # Add shaded areas for overbought/oversold zones
        fig.add_hrect(
            y0=70, y1=100,
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0
        )
        fig.add_hrect(
            y0=0, y1=30,
            fillcolor="green", opacity=0.1,
            layer="below", line_width=0
        )

        # Add RSI line in purple
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            name="RSI",
            line=dict(color='purple')
        ))

        # Add RSI MA line in yellow
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI_MA3'],
            name="RSI (3 MA)",
            line=dict(color='yellow', dash='dot')
        ))

        # Add reference lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5)

        return json.loads(fig.to_json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# %%
