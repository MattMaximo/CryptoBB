from fastapi import APIRouter, HTTPException
from app.services.velo_service import VeloService
from app.assets.charts.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

velo_router = APIRouter()
velo_service = VeloService()


@velo_router.get("/futures-products")
async def get_velo_futures_products():
    data = velo_service.get_futures_products()
    return data.to_dict(orient="records")

@velo_router.get("/spot-products")
async def get_velo_spot_products():
    data = velo_service.get_spot_products()
    return data.to_dict(orient="records")

@velo_router.get("/options-products")
async def get_velo_options_products():
    data = velo_service.get_options_products()
    return data.to_dict(orient="records")

@velo_router.get("/oi-weighted-funding-rates")
async def get_velo_oi_weighted_funding_rates(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.oi_weighted_funding_rate(coin, begin, resolution)
        data = data.set_index("time")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="OI Weighted Funding Rate"
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
            line=dict(color="#F7931A"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        figure.update_layout(
            yaxis=dict(
                tickformat=".0%",  # Format as percentage with no decimals
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff",
            )
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@velo_router.get("/exchange-funding-rates")
async def get_velo_funding_rates(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        # Get data from velo service
        data = velo_service.funding_rates(coin, begin, resolution)
        data['time'] = pd.to_datetime(data['time'])
        # Define colors for exchanges
        colors = {
            'binance-futures': '#F3BA2F',  # Binance yellow
            'bybit': '#4982D4',           # Bybit blue
            'okex-swap': '#BB81F6',       # OKX purple
            'hyperliquid': '#50D2C1'      # HL Green
        }

        # Create Plotly Figure
        figure = go.Figure(layout=create_base_layout(
            x_title="Date",
            y_title="Annualized Funding Rate (%)",
            y_dtype=".2%"
        ))

        # Group by exchange and add a trace for each
        for exchange, group_data in data.groupby('exchange'):
            figure.add_trace(
                go.Scatter(
                    x=group_data['time'],
                    y=group_data['annualized_funding_rate'],
                    mode='lines',
                    name=exchange,
                    line=dict(color=colors.get(exchange, '#000000'))  # Default to black if exchange is not in colors
                )
            )

        # Return the chart as JSON
        return json.loads(figure.to_json())

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing funding rates: {str(e)}")

@velo_router.get("/long-liquidations")
async def get_velo_long_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum'
        }).reset_index()
        data = data.set_index("time")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Long Liquidations"
            )
        )

        # Add bar chart for liquidations
        figure.add_bar(
            x=data.index,
            y=data["buy_liquidations_dollar_volume"],
            name="Long Liquidations",
            marker_color="rgba(255,0,0,0.5)"
        )

        # Update layout for secondary y-axis and hover mode
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            hovermode='x unified'
        )

        # Add price line
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#F7931A"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/short-liquidations")
async def get_velo_short_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        data = data.rename(columns={"time": "date"})
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Short Liquidations"
            )
        )

        figure.add_bar(
            x=data.index,
            y=data["sell_liquidations_dollar_volume"],
            name="Short Liquidations",
            marker=dict(color="#ff0000")
        )

        # Update layout for secondary y-axis and hover mode
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            hovermode='x unified'
        )

        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#ffffff"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/net-liquidations")
async def get_velo_net_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum',
            'sell_liquidations_dollar_volume': 'sum'
        }).reset_index()
        
        data['net_liquidations'] = data['buy_liquidations_dollar_volume'] - data['sell_liquidations_dollar_volume']
        data = data.set_index("time")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Net Liquidations ($)"
            )
        )

        # Add bar chart with conditional colors
        figure.add_bar(
            x=data.index,
            y=data["net_liquidations"],
            name="Net Liquidations",
            marker_color=['rgba(0,255,0,0.5)' if x >= 0 else 'rgba(255,0,0,0.5)' 
                        for x in data["net_liquidations"]]
        )

        # Update layout for secondary y-axis
        figure.update_layout(
            yaxis2=dict(
                title="Price ($)",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            hovermode='x unified'
        )

        # Add price line
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#F7931A"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/open-interest")
async def get_velo_open_interest(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.open_interest(coin, begin, resolution)
        
        oi_data = data.groupby(['time', 'exchange'])['dollar_open_interest_close'].sum().reset_index()
        price_data = data.groupby('time')['close_price'].mean().reset_index()
        
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Open Interest ($)"
            )
        )

        # Define exchange colors
        colors = {
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
                    line=dict(color=colors[exchange]),
                )
            )

        # Update layout for secondary y-axis
        figure.update_layout(
            yaxis=dict(
                title="Open Interest ($)",
                gridcolor="#2f3338",
                color="#ffffff",
            ),
            yaxis2=dict(
                title="Price ($)", 
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            hovermode='x unified'
        )

        # Add price line
        figure.add_trace(
            go.Scatter(
                x=price_data['time'],
                y=price_data['close_price'],
                name="Price",
                line=dict(color="#ffffff"),
                yaxis="y2",
                hovertemplate="%{y:,.2f}"
            )
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@velo_router.get("/ohlcv")
async def get_velo_ohlcv(ticker: str = "BTCUSDT", exchange: str = "binance", resolution: str = "1d"):
    try:
        from highcharts_stock.options.series.candlestick import CandlestickSeries
        from highcharts_stock.options.chart import ChartOptions
        from highcharts_stock.chart import Chart
        
        # Get data from velo service
        data = velo_service.get_ohlcv(ticker, exchange, resolution)
                
        # Create data points for Highcharts - format: [timestamp, open, high, low, close]
        chart_data = [[
            row['time'],  # timestamp is already in milliseconds
            row['open_price'],
            row['high_price'],
            row['low_price'],
            row['close_price'],
        ] for _, row in data.iterrows()]

        chart = Chart()
        
        # Configure chart options
        chart.chart = ChartOptions(
            type='candlestick',            
            style={
                'fontFamily': 'Arial, sans-serif'
            }
        )

        chart.add_series(CandlestickSeries(
            data=chart_data,
            name=ticker,
            tooltip={
                'valueDecimals': 2
            },
        ))

        obj = json.loads(chart.to_json())
        obj["constructorType"] = "stockChart"
        return obj

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@velo_router.get("/basis")
async def get_velo_basis(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.basis(coin.upper(), begin, resolution)
        data = data.groupby('time', as_index=False)['3m_basis_ann'].mean()
        data = data.set_index("time")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="3m Basis Ann %",
                y_dtype=".0%"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["3m_basis_ann"],
            mode="lines",
            name="3m Basis Ann",
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))