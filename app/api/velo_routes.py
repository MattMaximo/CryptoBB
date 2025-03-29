from fastapi import APIRouter, HTTPException
from app.services.velo_service import VeloService
from app.core.plotly_config import (
    get_chart_colors, 
    apply_config_to_figure,
    create_base_layout
)
from app.core.registry import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

velo_router = APIRouter()
velo_service = VeloService()


@velo_router.get("/futures-products")
@register_widget({
    "name": "Velo Futures Products",
    "description": "List of all available futures products on exchanges",
    "category": "crypto",
    "endpoint": "velo/futures-products",
    "isUtility": True,
    "source": "VeloData",
})
async def get_velo_futures_products():
    data = velo_service.get_futures_products()
    return data.to_dict(orient="records")

@velo_router.get("/spot-products")
@register_widget({
    "name": "Velo Spot Products",
    "description": "List of all available spot products on exchanges",
    "category": "crypto",
    "endpoint": "velo/spot-products",
    "isUtility": True,
    "source": "VeloData",
})
async def get_velo_spot_products():
    data = velo_service.get_spot_products()
    return data.to_dict(orient="records")

@velo_router.get("/options-products")
@register_widget({
    "name": "Velo Options Products",
    "description": "List of all available options products on exchanges",
    "category": "crypto",
    "endpoint": "velo/options-products",
    "isUtility": True,
    "source": "VeloData",
})
async def get_velo_options_products():
    data = velo_service.get_options_products()
    return data.to_dict(orient="records")

@velo_router.get("/oi-weighted-funding-rates")
@register_widget({
    "name": "OI Weighted Funding Rates",
    "description": "Open Interest weighted funding rates across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/oi-weighted-funding-rates",
    "gridData": {"w": 40, "h": 11},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_oi_weighted_funding_rates(
    coin: str = "BTC", 
    begin: str = None, 
    resolution: str = "1d", 
    theme: str = "dark"
):
    try:
        data = velo_service.oi_weighted_funding_rate(coin, begin, resolution)
        data = data.set_index("time")
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="OI Weighted Funding Rate",
                theme=theme
            )
        )

        # Add bar chart for funding rate
        figure.add_bar(
            x=data.index,
            y=data["oi_weighted_funding_rate_annualized"],
            name="OI Weighted Funding Rate",
            marker_color=['rgba(0,255,0,0.3)' if x >= 0 else 'rgba(255,0,0,0.3)' 
                        for x in data["oi_weighted_funding_rate_annualized"]],
            hovertemplate="%{y:.2%}"
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color=colors['main_line']),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        figure.update_layout(
            yaxis=dict(
                tickformat=".0%",  # Format as percentage with no decimals
            ),
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
            )
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@velo_router.get("/exchange-funding-rates")
@register_widget({
    "name": "Exchange Funding Rates",
    "description": "Funding rates across different exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/exchange-funding-rates",
    "gridData": {"w": 40, "h": 11},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_funding_rates(
    coin: str = "BTC", 
    begin: str = None, 
    resolution: str = "1d", 
    theme: str = "dark"
):
    try:
        # Get data from velo service
        data = velo_service.funding_rates(coin, begin, resolution)
        data['time'] = pd.to_datetime(data['time'])
        
        # Define colors for exchanges
        exchange_colors = {
            'binance-futures': '#F3BA2F',  # Binance yellow
            'bybit': '#4982D4',           # Bybit blue
            'okex-swap': '#BB81F6',       # OKX purple
            'hyperliquid': '#50D2C1'      # HL Green
        }

        # Create Plotly Figure
        figure = go.Figure(layout=create_base_layout(
            x_title="Date",
            y_title="Annualized Funding Rate (%)",
            y_dtype=".2%",
            theme=theme
        ))

        # Group by exchange and add a trace for each
        for exchange, group_data in data.groupby('exchange'):
            figure.add_trace(
                go.Scatter(
                    x=group_data['time'],
                    y=group_data['annualized_funding_rate'],
                    mode='lines',
                    name=exchange,
                    line=dict(color=exchange_colors.get(exchange, '#000000'))
                )
            )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Return the chart as JSON
        return json.loads(figure.to_json())

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing funding rates: {str(e)}")

@velo_router.get("/long-liquidations")
@register_widget({
    "name": "Long Liquidations",
    "description": "Long position liquidations across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/long-liquidations",
    "gridData": {"w": 20, "h": 12},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_long_liquidations(
    coin: str = "BTC", 
    begin: str = None, 
    resolution: str = "1d", 
    theme: str = "dark"
):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum'
        }).reset_index()
        data = data.set_index("time")
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Long Liquidations",
                theme=theme
            )
        )

        # Add bar chart for liquidations
        figure.add_bar(
            x=data.index,
            y=data["buy_liquidations_dollar_volume"],
            name="Long Liquidations",
            marker_color=colors['negative']
        )

        # Add price line
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color=colors['main_line']),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )
        
        # Update layout for secondary y-axis and hover mode
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
            ),
            hovermode='x unified'
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/short-liquidations")
@register_widget({
    "name": "Short Liquidations",
    "description": "Short position liquidations across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/short-liquidations",
    "gridData": {"w": 20, "h": 12},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
            "type": "text",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_short_liquidations(
    coin: str = "BTC", 
    begin: str = None, 
    resolution: str = "1d", 
    theme: str = "dark"
):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        data = data.rename(columns={"time": "date"})
        data = data.set_index("date")
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Short Liquidations",
                theme=theme
            )
        )

        figure.add_bar(
            x=data.index,
            y=data["sell_liquidations_dollar_volume"],
            name="Short Liquidations",
            marker_color=colors['negative']
        )

        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color=colors['main_line']),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )
        
        # Update layout for secondary y-axis and hover mode
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
            ),
            hovermode='x unified'
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/net-liquidations")
@register_widget({
    "name": "Net Liquidations",
    "description": "Net liquidations (long - short) across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/net-liquidations",
    "gridData": {"w": 40, "h": 12},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_net_liquidations(
    coin: str = "BTC", 
    begin: str = None, 
    resolution: str = "1d", 
    theme: str = "dark"
):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum',
            'sell_liquidations_dollar_volume': 'sum'
        }).reset_index()
        
        data['net_liquidations'] = (
            data['buy_liquidations_dollar_volume'] - 
            data['sell_liquidations_dollar_volume']
        )
        data = data.set_index("time")
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Net Liquidations ($)",
                theme=theme
            )
        )

        # Add bar chart with conditional colors
        figure.add_bar(
            x=data.index,
            y=data["net_liquidations"],
            name="Net Liquidations",
            marker_color=[
                colors['positive'] if x >= 0 else colors['negative'] 
                for x in data["net_liquidations"]
            ]
        )

        # Add price line
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color=colors['main_line']),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )
        
        # Update layout for secondary y-axis
        figure.update_layout(
            yaxis2=dict(
                title="Price ($)",
                overlaying="y",
                side="right",
            ),
            hovermode='x unified'
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/open-interest")
@register_widget({
    "name": "Open Interest",
    "description": "Open interest across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/open-interest",
    "gridData": {"w": 40, "h": 15},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_open_interest(coin: str = "BTC", begin: str = None, resolution: str = "1d", theme: str = "dark"):
    try:
        data = velo_service.open_interest(coin, begin, resolution)
        
        oi_data = data.groupby(['time', 'exchange'])['dollar_open_interest_close'].sum().reset_index()
        price_data = data.groupby('time')['close_price'].mean().reset_index()
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Open Interest ($)",
                theme=theme
            )
        )

        # Define exchange colors
        exchange_colors = {
            'binance-futures': '#F3BA2F',
            'bybit': '#4982D4',
            'okex-swap': '#BB81F6',
            'hyperliquid': '#50D2C1'
        }

        # Add stacked area for each exchange
        for exchange in oi_data['exchange'].unique():
            exchange_data = oi_data[oi_data['exchange'] == exchange]
            figure.add_trace(
                go.Scatter(
                    x=exchange_data['time'],
                    y=exchange_data['dollar_open_interest_close'],
                    name=exchange,
                    mode='lines',
                    stackgroup='oi',
                    line=dict(color=exchange_colors.get(exchange, colors['main_line'])),
                )
            )

        # Add price line
        figure.add_trace(
            go.Scatter(
                x=price_data['time'],
                y=price_data['close_price'],
                name="Price",
                line=dict(color=colors['main_line']),
                yaxis="y2",
                hovertemplate="%{y:,.2f}"
            )
        )
        
        # Update layout for secondary y-axis
        figure.update_layout(
            yaxis2=dict(
                title="Price ($)", 
                overlaying="y",
                side="right",
            ),
            hovermode='x unified'
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/ohlcv")
@register_widget({
    "name": "OHLCV Chart",
    "description": "Open, high, low, close, volume chart",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/ohlcv",
    "gridData": {"w": 40, "h": 21},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "candlestick"}},
})
async def get_velo_ohlcv(
    ticker: str = "BTCUSDT", 
    exchange: str = "binance", 
    resolution: str = "1d",
    theme: str = "dark"
):
    try:
        # Get data from velo service
        data = velo_service.get_ohlcv(ticker, exchange, resolution)
        
        if data.empty:
            raise HTTPException(status_code=404, detail="No data found for the specified parameters")
        
        # Convert to Plotly format instead of Highcharts
        figure = go.Figure()
        
        # Add candlestick trace
        figure.add_trace(
            go.Candlestick(
                x=data['time'],
                open=data['open_price'],
                high=data['high_price'],
                low=data['low_price'],
                close=data['close_price'],
                name=ticker,
                increasing_line_color='#00B140',  # Green for increasing candles
                decreasing_line_color='#F4284D',  # Red for decreasing candles
            )
        )
        
        # Add volume as a bar chart at the bottom with a separate y-axis
        figure.add_trace(
            go.Bar(
                x=data['time'],
                y=data['coin_volume'],
                name='Volume',
                marker_color='rgba(128, 128, 128, 0.5)',
                yaxis='y2',
                hovertemplate='Volume: %{y:,.0f}<extra></extra>'
            )
        )
        
        # Set up the layout with theme-based styling
        dark_theme = theme == 'dark'
        bg_color = '#121212' if dark_theme else '#FFFFFF'
        text_color = '#FFFFFF' if dark_theme else '#333333'
        grid_color = 'rgba(255,255,255,0.1)' if dark_theme else 'rgba(0,0,0,0.1)'
        
        # Create base layout
        layout = create_base_layout(
            x_title="Date",
            y_title="Price",
            theme=theme
        )
        
        # Update layout for candlestick chart
        figure.update_layout(
            layout,
            title=f"{ticker} on {exchange.capitalize()}",
            xaxis_rangeslider_visible=False,  # Hide the range slider
            yaxis=dict(
                title="Price",
                side="left",
                showgrid=True,
                gridcolor=grid_color,
            ),
            yaxis2=dict(
                title="Volume",
                overlaying="y",
                side="right",
                showgrid=False,
                rangemode='normal',
                anchor="x",
            ),
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)
        
        return json.loads(figure.to_json())
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@velo_router.get("/basis")
@register_widget({
    "name": "Annualized Basis",
    "description": "Annualized basis across exchanges",
    "category": "crypto",
    "type": "chart",
    "endpoint": "velo/basis",
    "gridData": {"w": 40, "h": 17},
    "source": "VeloData",
    "params": [
        {
            "paramName": "coin",
            "value": "BTC",
            "label": "Coin",
            "show": True,
            "description": "Cryptocurrency to display data for",
        },
        {
            "paramName": "resolution",
            "value": "1d",
            "label": "Resolution",
            "show": True,
            "description": "Time resolution for data points",
            "type": "endpoint",
            "optionsEndpoint": "velo/resolution-options",
        },
        {
            "paramName": "begin",
            "value": "2024-01-01",
            "label": "Start Date",
            "show": True,
            "description": "Start date for the data",
            "type": "date",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_velo_basis(coin: str = "BTC", begin: str = None, resolution: str = "1d", theme: str = "dark"):
    try:
        data = velo_service.basis(coin.upper(), begin, resolution)
        data = data.groupby('time', as_index=False)['3m_basis_ann'].mean()
        data = data.set_index("time")
        
        # Get theme-based colors
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="3m Basis Ann %",
                y_dtype=".0%",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["3m_basis_ann"],
            mode="lines",
            name="3m Basis Ann",
            line=dict(color=colors['main_line']),
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/resolution-options")
async def get_resolution_options():
    """
    Returns a formatted list of resolution options in the format:
    {
        "value": "1h",
        "label": "1 Hour"
    }
    """
    resolution_options = [
        {"value": "1m", "label": "1 Minute"},
        {"value": "5m", "label": "5 Minutes"},
        {"value": "30m", "label": "30 Minutes"},
        {"value": "1h", "label": "1 Hour"},
        {"value": "4h", "label": "4 Hours"},
        {"value": "12h", "label": "12 Hours"},
        {"value": "24h", "label": "1 Day"},
    ]
    
    return resolution_options