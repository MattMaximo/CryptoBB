from fastapi import APIRouter, HTTPException
from app.services.coingecko_service import CoinGeckoService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
import plotly.graph_objects as go
import pandas as pd
import json


coingecko_router = APIRouter()

# Initialize the CoinGecko service
coingecko_service = CoinGeckoService()

@coingecko_router.get("/coin-list")
async def get_coin_list(
    include_platform: str = "true", 
    status: str = "active"
):
    symbols_list = await coingecko_service.get_coin_list(include_platform, status)
    return symbols_list.to_dict(orient="records")


@coingecko_router.get("/price")
async def get_market_data(coin_id: str, theme: str = "dark"):
    try:
        coin_id = coin_id.lower()
        # Get price data directly from the service
        data = await coingecko_service.get_market_data(coin_id)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price (USD)",
                y_dtype=".2f",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data[f"{coin_id}_price"],
            mode="lines",
            name="Price",
            line=dict(color=colors['main_line']),
        )

        # Apply the standard configuration to the figure with theme
        figure, config = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        # Add config to the figure dictionary
        figure_dict["config"] = config
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/dominance")
async def get_dominance(coin_id: str, theme: str = "dark"):
    try:
        coin_id = coin_id.lower()
        # Get dominance data directly from the service
        data = await coingecko_service.get_dominance(coin_id)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Dominance (%)",
                y_dtype=".2f",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["dominance"] * 100,
            mode="lines",
            name="Dominance",
            line=dict(color=colors['main_line']),
            hovertemplate="%{y:.2f}%"  # Display hover as percentage
        )

        if coin_id == "bitcoin":
            figure.add_hline(
                y=40,
                line_color=colors['negative'],
                line_dash="dash",
                annotation_text="Top",
                annotation_position="bottom right",
            )
            figure.add_hline(
                y=65,
                line_color=colors['positive'],
                line_dash="dash",
                annotation_text="Bottom",
                annotation_position="top right",
            )

        # Apply the standard configuration to the figure with theme
        figure, config = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        # Add config to the figure dictionary
        figure_dict["config"] = config
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/vm-ratio")
async def get_vm_ratio(coin_id: str, theme: str = "dark"):
    try:
        coin_id = coin_id.lower()
        data = await coingecko_service.get_market_data(coin_id)
        # Fix the column name from _total_volume to _volume
        columns = [
            "date", 
            f"{coin_id}_price", 
            f"{coin_id}_market_cap", 
            f"{coin_id}_volume"
        ]
        data = data[columns]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        # Update the calculation to use _volume instead of _total_volume
        market_cap_col = f"{coin_id}_market_cap"
        volume_col = f"{coin_id}_volume"
        data["vm_ratio"] = data[volume_col] / data[market_cap_col]
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Volume/Market Cap Ratio",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["vm_ratio"],
            mode="lines",
            name="Ratio",  # Added name to specify the trace name in the legend
            line=dict(color=colors['main_line']),
            hovertemplate="%{y:.2f}"  # Format hover as decimal
        )
        # Override tick format to show decimals
        figure.update_yaxes(tickformat=".2f")

        # Apply the standard configuration to the figure with theme
        figure, config = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        # Add config to the figure dictionary
        figure_dict["config"] = config
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@coingecko_router.get("/correlation")
async def get_correlation(coin_id1: str, coin_id2: str, theme: str = "dark"):
    try:
        coin_id1 = coin_id1.lower()
        coin_id2 = coin_id2.lower()
        
        data1 = await coingecko_service.get_market_data(coin_id1)
        data2 = await coingecko_service.get_market_data(coin_id2)
        
        # Merge the data on date
        merged_data = pd.merge(
            data1[["date", f"{coin_id1}_price"]], 
            data2[["date", f"{coin_id2}_price"]], 
            on="date"
        )
        
        merged_data["date"] = pd.to_datetime(merged_data["date"]).dt.strftime("%Y-%m-%d")
        merged_data = merged_data.set_index("date")
        
        # Get chart colors based on theme
        colors = get_chart_colors(theme)
        
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title=f"{coin_id1.upper()} Price",
                theme=theme
            )
        )

        figure.add_scatter(
            x=merged_data.index,
            y=merged_data[f"{coin_id1}_price"],
            mode="lines",
            line=dict(color=colors['main_line']),
            name=f"{coin_id1.upper()} Price"
        )

        figure.add_scatter(
            x=merged_data.index,
            y=merged_data[f"{coin_id2}_price"],
            mode="lines",
            line=dict(color=colors['secondary']),
            name=f"{coin_id2.upper()} Price"
        )

        # Apply the standard configuration to the figure with theme
        figure, config = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        # Add config to the figure dictionary
        figure_dict["config"] = config
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@coingecko_router.get("/btc-price-sma-multiplier")
async def get_btc_price_sma_multiplier(theme: str = "dark"):
    try:
        data = await coingecko_service.get_market_data("bitcoin")
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data[["date", "bitcoin_price"]]
        data = data.set_index("date")

        sma_days = 1458
        data['SMA_1458'] = data['bitcoin_price'].rolling(window=sma_days).mean()
        data['multiplier'] = data['bitcoin_price'] / data['SMA_1458']

        # Get chart colors based on theme
        colors = get_chart_colors(theme)
        
        # Define color schemes based on theme
        if theme == "dark":
            color_map = {
                'very_low': '#00ff00',    # Bright green
                'low': '#ffff00',         # Bright yellow
                'medium': '#ffa500',      # Bright orange
                'high': '#ff0000',        # Bright red
                'very_high': '#ff00ff',   # Bright magenta
                'extreme': '#00ffff',     # Bright cyan
                'ultra': '#0080ff',       # Bright blue
                'max': '#ffffff'          # White
            }
        else:
            color_map = {
                'very_low': '#008800',    # Dark green
                'low': '#888800',         # Dark yellow
                'medium': '#884400',      # Dark orange
                'high': '#880000',        # Dark red
                'very_high': '#880088',   # Dark magenta
                'extreme': '#008888',     # Dark cyan
                'ultra': '#0044aa',       # Dark blue
                'max': '#000000'          # Black
            }

        def get_color(multiplier):
            if multiplier < 1.5:
                return color_map['very_low']
            elif 1.5 <= multiplier < 2:
                return color_map['low']
            elif 2 <= multiplier < 2.5:
                return color_map['medium']
            elif 2.5 <= multiplier < 3:
                return color_map['high']
            elif 3 <= multiplier < 4:
                return color_map['very_high']
            elif 4 <= multiplier < 5:
                return color_map['extreme']
            elif 5 <= multiplier < 6:
                return color_map['ultra']
            else:
                return color_map['max']

        data['color'] = data['multiplier'].apply(get_color)
        data = data.dropna(subset=['SMA_1458'])

        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                theme=theme
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
            line=dict(color=colors['sma_line'], dash='dash'),
            name='SMA-1458'
        ))

        # Update layout for the plot
        fig.update_layout(
            yaxis_type='log',
            showlegend=False
        )

        # Apply the standard configuration to the figure with theme
        fig, config = apply_config_to_figure(fig, theme=theme)

        # Convert figure to JSON with the config
        fig_json = fig.to_json()
        fig_dict = json.loads(fig_json)
        
        # Add config to the figure dictionary
        fig_dict["config"] = config
        
        return fig_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@coingecko_router.get("/coin-list-formatted")
async def get_coin_list_formatted(
    include_platform: str = "true", 
    status: str = "active"
):
    """
    Returns a formatted list of coins in the format:
    {
        "value": "bitcoin",
        "label": "Bitcoin (BTC)"
    }
    """
    symbols_list = await coingecko_service.get_coin_list(include_platform, status)
    
    # Convert to the requested format
    formatted_list = []
    for coin in symbols_list.to_dict(orient="records"):
        formatted_list.append({
            "value": coin["id"],
            "label": f"{coin['name']} ({coin['symbol'].upper()})"
        })
    
    return formatted_list
