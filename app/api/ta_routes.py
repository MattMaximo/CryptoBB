from fastapi import APIRouter, HTTPException
from app.services.ccdata_service import CCDataService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json
import numpy as np

ta_router = APIRouter()

ccdata_service = CCDataService()

@ta_router.get("/rsi")
async def get_rsi(exchange: str, symbol: str, interval: str, aggregate: int):
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


@ta_router.get("/macd")
async def get_macd(exchange: str, symbol: str, interval: str, aggregate: int):
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

        # Calculate MACD components
        exp1 = data['CLOSE'].ewm(span=12, adjust=False).mean()
        exp2 = data['CLOSE'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['Histogram'] = data['MACD'] - data['Signal']

        # Calculate dynamic threshold levels (based on historical volatility)
        upper_threshold = data['MACD'].quantile(0.85)
        lower_threshold = data['MACD'].quantile(0.15)

        # Create the chart with modified layout
        layout = create_base_layout(x_title="Date", y_title="MACD", y_dtype="d")
        layout.update(
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                zerolinecolor='gray',
                zerolinewidth=1
            ),
            xaxis=dict(
                showgrid=False
            )
        )

        fig = go.Figure(layout=layout)
        
        # Add shaded areas for overbought/oversold zones
        fig.add_hrect(
            y0=upper_threshold, y1=data['MACD'].max(),
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0
        )
        fig.add_hrect(
            y0=data['MACD'].min(), y1=lower_threshold,
            fillcolor="green", opacity=0.1,
            layer="below", line_width=0
        )

        # Add MACD line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MACD'],
            name="MACD",
            line=dict(color='purple', width=2)
        ))

        # Add Signal line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Signal'],
            name="Signal",
            line=dict(color='yellow', width=2, dash='dot')
        ))

        # Add Histogram with increased transparency
        fig.add_trace(go.Bar(
            x=data.index,
            y=data['Histogram'],
            name="Histogram",
            marker=dict(
                color=data['Histogram'].apply(
                    lambda x: 'rgba(0, 255, 0, 0.3)' if x > 0 else 'rgba(255, 0, 0, 0.3)'
                )
            )
        ))

        # Add reference lines for buy/sell zones
        fig.add_hline(y=upper_threshold, line_dash="dash", line_color="red", opacity=0.5,
                     annotation=dict(text="Sell Zone", x=1.02, xanchor="left"))
        fig.add_hline(y=lower_threshold, line_dash="dash", line_color="green", opacity=0.5,
                     annotation=dict(text="Buy Zone", x=1.02, xanchor="left"))
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

        return json.loads(fig.to_json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ta_router.get("/fibonacci-retracement")
async def get_fibonacci(exchange: str, symbol: str, interval: str, aggregate: int):
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

        threshold_multiplier=3
        depth=10
        reverse=False

        # Calculate pivots based on thresholds
        data['HighPivot'] = (data['HIGH'] > data['HIGH'].shift(1)) & \
                           (data['HIGH'] > data['HIGH'].shift(-1))
        data['LowPivot'] = (data['LOW'] < data['LOW'].shift(1)) & \
                           (data['LOW'] < data['LOW'].shift(-1))

        # Get high pivot points and their values
        high_pivots = data[data['HighPivot']]['HIGH']
        low_pivots = data[data['LowPivot']]['LOW']

        if len(high_pivots) == 0 or len(low_pivots) == 0:
            raise ValueError("Not enough data to calculate Fibonacci retracement levels.")

        # Get the most recent swing high and swing low
        last_high = high_pivots.iloc[-1]
        last_low = low_pivots.iloc[-1]

        # Determine start and end prices based on reverse flag
        start_price = last_high if not reverse else last_low
        end_price = last_low if not reverse else last_high
        height = start_price - end_price

        # Calculate Fibonacci levels
        fibonacci_ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.414, 1.618, 2.618, 3.618, 4.236]
        levels = {
            f"Level {ratio}": start_price - height * ratio for ratio in fibonacci_ratios
        }

        # Create a DataFrame for visualization or further analysis
        levels_df = pd.DataFrame(list(levels.items()), columns=['Level', 'Price'])
        return levels_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ta_router.get("/stochastic")
async def get_stochastic(exchange: str, symbol: str, interval: str, aggregate: int):
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

        # Calculate Stochastic Oscillator
        period = 14
        low_min = data['LOW'].rolling(window=period).min()
        high_max = data['HIGH'].rolling(window=period).max()
        
        # Calculate %K
        data['%K'] = 100 * ((data['CLOSE'] - low_min) / (high_max - low_min))
        
        # Calculate %D (3-period MA of %K)
        data['%D'] = data['%K'].rolling(window=3).mean()

        # Create the chart with modified layout
        layout = create_base_layout(x_title="Date", y_title="Stochastic", y_dtype="d")
        layout.update(
            yaxis=dict(
                range=[0, 100],
                showgrid=False,
                dtick=20
            ),
            xaxis=dict(
                showgrid=False
            )
        )

        fig = go.Figure(layout=layout)
        
        # Add shaded areas for overbought/oversold zones
        fig.add_hrect(
            y0=80, y1=100,
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0
        )
        fig.add_hrect(
            y0=0, y1=20,
            fillcolor="green", opacity=0.1,
            layer="below", line_width=0
        )

        # Add %K line (fast) in purple
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['%K'],
            name="%K",
            line=dict(color='purple', width=2)
        ))

        # Add %D line (slow) in yellow
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['%D'],
            name="%D",
            line=dict(color='yellow', width=2, dash='dot')
        ))

        # Add reference lines
        fig.add_hline(y=80, line_dash="dash", line_color="red", opacity=0.5,
                     annotation=dict(text="Overbought", x=1.02, xanchor="left"))
        fig.add_hline(y=20, line_dash="dash", line_color="green", opacity=0.5,
                     annotation=dict(text="Oversold", x=1.02, xanchor="left"))

        return json.loads(fig.to_json())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

