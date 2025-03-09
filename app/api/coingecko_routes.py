from fastapi import APIRouter, HTTPException
from app.services.coingecko_service import CoinGeckoService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
from app.core.widget_decorator import register_widget
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
@register_widget({
    "name": "Coingecko Correlation",
    "description": "Historical correlation between two search tokens",
    "category": "crypto",
    "defaultViz": "chart",
    "endpoint": "coingecko/correlation",
    "gridData": {"w": 20, "h": 9},
    "source": "CoinGecko",
    "params": [
        {
            "paramName": "coin_id1",
            "value": "bitcoin",
            "label": "Coin",
            "show": True,
            "type": "endpoint",
            "optionsEndpoint": "coingecko/coin-list-formatted",
            "description": "CoinGecko ID of the first cryptocurrency",
            "style": {"popupWidth": 600},
        },
        {
            "paramName": "coin_id2",
            "value": "ethereum",
            "label": "Coin",
            "show": True,
            "type": "endpoint",
            "optionsEndpoint": "coingecko/coin-list-formatted",
            "description": "CoinGecko ID of the second cryptocurrency",
            "style": {"popupWidth": 600},
        },
        {
            "type": "date",
            "paramName": "start_date",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "The start date for the data",
        },
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_correlation(
    coin_id1: str, 
    coin_id2: str, 
    start_date: str = "2025-01-01", 
    theme: str = "dark"
):
    try:
        coin_id1 = coin_id1.lower()
        coin_id2 = coin_id2.lower()
        
        # Get market data for both coins
        data1 = await coingecko_service.get_market_data(coin_id1)
        data2 = await coingecko_service.get_market_data(coin_id2)
        
        # Ensure data is not empty
        if data1.empty or data2.empty:
            raise ValueError(
                f"No data available for one or both coins: {coin_id1}, {coin_id2}"
            )
        
        # Check if price columns exist
        price_col1 = f"{coin_id1}_price"
        price_col2 = f"{coin_id2}_price"
        
        if price_col1 not in data1.columns:
            raise ValueError(f"Price column {price_col1} not found in data")
        if price_col2 not in data2.columns:
            raise ValueError(f"Price column {price_col2} not found in data")
        
        # Convert date columns to datetime for filtering
        data1["date"] = pd.to_datetime(data1["date"])
        data2["date"] = pd.to_datetime(data2["date"])
        
        # Filter by start_date if provided
        if start_date:
            start_date = pd.to_datetime(start_date)
            data1 = data1[data1["date"] >= start_date]
            data2 = data2[data2["date"] >= start_date]
            
            # Check if filtered data is empty
            if data1.empty or data2.empty:
                raise ValueError(
                    f"No data available after {start_date} for one or both coins"
                )
        
        # Merge the data on date
        merged_data = pd.merge(
            data1[["date", price_col1]], 
            data2[["date", price_col2]], 
            on="date",
            how="inner"  # Only keep dates that exist in both datasets
        )
        
        # Check if merged data is empty
        if merged_data.empty:
            raise ValueError(
                "No overlapping dates found between the two coins"
            )
        
        # Calculate correlation before setting index
        correlation = merged_data[price_col1].corr(merged_data[price_col2])
        
        # Format date after calculations
        merged_data["date_str"] = merged_data["date"].dt.strftime("%Y-%m-%d")
        merged_data = merged_data.set_index("date_str")
        
        # Get chart colors based on theme
        colors = get_chart_colors(theme)
        
        # Create figure with dual y-axes for different price scales
        figure = go.Figure()
        
        # Set base layout
        figure.update_layout(
            **create_base_layout(
                x_title="Date",
                y_title=f"{coin_id1.upper()} Price",
                theme=theme
            )
        )
        
        # Add second y-axis with color matching the second line
        figure.update_layout(
            yaxis=dict(
                title=dict(
                    text=f"{coin_id1.upper()} Price",
                    font=dict(color=colors['main_line'])
                )
            ),
            yaxis2=dict(
                title=dict(
                    text=f"{coin_id2.upper()} Price",
                    font=dict(color=colors['secondary'])
                ),
                overlaying="y",
                side="right",
                showgrid=False
            )
        )
        
        # Add first coin to primary y-axis
        figure.add_scatter(
            x=merged_data.index,
            y=merged_data[price_col1],
            mode="lines",
            line=dict(color=colors['main_line']),
            name=f"{coin_id1.upper()} Price"
        )
        
        # Add second coin to secondary y-axis
        figure.add_scatter(
            x=merged_data.index,
            y=merged_data[price_col2],
            mode="lines",
            line=dict(color=colors['secondary']),
            name=f"{coin_id2.upper()} Price",
            yaxis="y2"
        )
        
        # Add correlation annotation with theme-appropriate color
        correlation_color = "white" if theme == "dark" else "black"
        figure.add_annotation(
            x=0.02,
            y=0.98,
            xref="paper",
            yref="paper",
            text=f"Correlation: {correlation:.2f}",
            showarrow=False,
            font=dict(
                color=correlation_color,
                size=14
            ),
            borderwidth=1,
            borderpad=4
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
                marker=dict(color=color, size=3),  # Reduced marker size from 5 to 3
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
            "label": f"{coin['name']} ({coin['symbol'].upper()})",
            "extraInfo": {
                "description": coin['name']
            }
        })
    
    return formatted_list
