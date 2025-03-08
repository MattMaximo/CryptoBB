from fastapi import APIRouter, HTTPException
from app.services.coingecko_service import CoinGeckoService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

coingecko_router = APIRouter()
coingecko_service = CoinGeckoService()


@coingecko_router.get("/coin-list")
async def get_coin_list(include_platform: str = "true", status: str = "active"):
    symbols_list = await coingecko_service.get_coin_list(include_platform, status)
    return symbols_list.to_dict(orient="records")

@coingecko_router.get("/price")
async def get_market_data(coin_id: str):
    try:
        coin_id = coin_id.lower()
        data = await coingecko_service.get_market_data(coin_id)
        data = data[["date", f"{coin_id}_price"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data[f"{coin_id}_price"],
            mode="lines",
            name="Price",
            line=dict(color="#E3BF1E"),
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/dominance")
async def get_dominance(coin_id: str):
    try:
        coin_id = coin_id.lower()
        data = await coingecko_service.get_dominance(coin_id)
        print(data)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Dominance (%)"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["dominance"] * 100,
            mode="lines",
            line=dict(color="#E3BF1E"),
            hovertemplate="%{y:.2f}%"  # Display hover as percentage
        )

        if coin_id == "bitcoin":
            figure.add_hline(
                y=40,
                line_color="red",
                line_dash="dash",
                annotation_text="Top",
                annotation_position="bottom right",
            )
            figure.add_hline(
                y=65,
                line_color="green",
                line_dash="dash",
                annotation_text="Bottom",
                annotation_position="top right",
            )

            figure.update_layout(
                uirevision='constant',  # Maintains view state during updates
                autosize=True,  # Enables auto-sizing for responsive behavior
                dragmode='zoom',  # Sets default mode to zoom instead of pan
                hovermode='closest',  # Improves hover experience
                clickmode='event',  # Makes clicking more responsive
                transition={
                    'duration': 50,  # Small transition for smoother feel
                    'easing': 'cubic-in-out'  # Smooth easing function
                },
                modebar={
                    'orientation': 'v',  # Vertical orientation for modebar
                    'activecolor': '#9ED3CD'  # Highlight color for active buttons
                },
                xaxis={
                    'rangeslider': {'visible': False},  # Disable rangeslider
                    'autorange': True,  # Enable autorange
                    'constrain': 'domain'  # Constrain to domain for better zoom
                },
                yaxis={
                    'autorange': True,  # Enable autorange
                    'constrain': 'domain',  # Constrain to domain
                    'fixedrange': False  # Allow y-axis zooming
                }
            )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/vm-ratio")
async def get_vm_ratio(coin_id: str):
    try:
        coin_id = coin_id.lower()
        data = await coingecko_service.get_vm_ratio(coin_id)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Ratio"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["vm_ratio"],
            mode="lines",
            name="Ratio",  # Added name to specify the trace name in the legend
            line=dict(color="#E3BF1E"),
            hovertemplate="%{y:.2f}"  # Format hover as decimal
        )
        figure.update_yaxes(tickformat=".2f")  # Override tick format to show decimals

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/correlation")
async def get_correlation(coin_id1: str, coin_id2: str):
    try:
        coin_id1 = coin_id1.lower()
        coin_id2 = coin_id2.lower()
        data = await coingecko_service.get_correlation(coin_id1, coin_id2)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Correlation"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["correlation"],
            mode="lines",
            line=dict(color="#E3BF1E")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@coingecko_router.get("/btc-price-sma-multiplier")
async def get_btc_price_sma_multiplier():
    try:
        data = await coingecko_service.get_market_data("bitcoin")
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data[["date", "bitcoin_price"]]
        data = data.set_index("date")

        sma_days = 1458
        data['SMA_1458'] = data['bitcoin_price'].rolling(window=sma_days).mean()
        data['multiplier'] = data['bitcoin_price'] / data['SMA_1458']

        def get_color(multiplier):
            if multiplier < 1.5:
                return '#00ff00'  # Bright green
            elif 1.5 <= multiplier < 2:
                return '#ffff00'  # Bright yellow
            elif 2 <= multiplier < 2.5:
                return '#ffa500'  # Bright orange
            elif 2.5 <= multiplier < 3:
                return '#ff0000'  # Bright red
            elif 3 <= multiplier < 4:
                return '#ff00ff'  # Bright magenta
            elif 4 <= multiplier < 5:
                return '#00ffff'  # Bright cyan
            elif 5 <= multiplier < 6:
                return '#0080ff'  # Bright blue
            else:
                return '#ffffff'  # White

        data['color'] = data['multiplier'].apply(get_color)
        data = data.dropna(subset=['SMA_1458'])

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                y_dtype=".2f"
            )
        )

        for color in data['color'].unique():
            subset = data[data['color'] == color]
            fig.add_trace(go.Scatter(
                x=subset.index,
                y=subset['bitcoin_price'],
                mode='markers',
                marker=dict(color=color, size=5),
                name=color
            ))

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['SMA_1458'],
            mode='lines',
            line=dict(color='white', dash='dash'),
            name='SMA-1458'
        ))

        # Update layout for the plot
        fig.update_layout(
            yaxis_type='log',
            showlegend=False
        )

        return json.loads(fig.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

