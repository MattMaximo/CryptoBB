from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.coingecko_service import CoinGeckoService
from app.services.glassnode_service import GlassnodeService
from app.services.google_trends_service import GoogleTrendsService
from app.services.velo_service import VeloService
from app.services.aave_service import AaveService
from app.services.telegram_service import TelegramService
from app.core.widgets import WIDGETS
from app.assets.aave_pools import AAVE_POOLS
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import pandas as pd

router = APIRouter()
coingecko_service = CoinGeckoService()
glassnode_service = GlassnodeService()
google_trends_service = GoogleTrendsService()
velo_service = VeloService()
aave_service = AaveService()
telegram_service = TelegramService()


@router.get("/widgets.json")
async def get_widgets():
    return WIDGETS


@router.get("/markets")
async def get_markets():
    data = coingecko_service.get_markets()
    return data.to_dict(orient="records")


@router.get("/coingecko_price")
async def get_market_data(coin_id: str):
    try:
        data = coingecko_service.get_market_data(coin_id)
        data = data[["date", f"{coin_id}_price"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Ratio", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data[f"{coin_id}_price"],
            mode="lines",
            line=dict(color="#00b0f0"),
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dominance")
async def get_dominance(coin_id: str):
    try:
        data = coingecko_service.get_dominance(coin_id)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Dominance", gridcolor="#2f3338", color="#ffffff"),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["dominance"], mode="lines", line=dict(color="#00b0f0")
        )

        if coin_id == "bitcoin":
            figure.add_hline(
                y=0.40,
                line_color="red",
                line_dash="dash",
                annotation_text="Top",
                annotation_position="bottom right",
            )
            figure.add_hline(
                y=0.65,
                line_color="green",
                line_dash="dash",
                annotation_text="Bottom",
                annotation_position="top right",
            )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vm_ratio")
async def get_vm_ratio(coin_id: str):
    try:
        data = coingecko_service.get_vm_ratio(coin_id)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Ratio", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["vm_ratio"], mode="lines", line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/coingecko_coin_list")
async def get_coin_list():
    symbols_list = coingecko_service.get_coin_list()
    return symbols_list.to_dict(orient="records")

@router.get("/lth_supply")
async def get_lth_supply(asset: str = "btc", show_price: str = "False"):
    try:
        data = glassnode_service.get_lth_supply(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="LTH Supply", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                showlegend=False,
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lth_supply"],
            mode="lines",
            name="LTH Supply",
            line=dict(color="#00b0f0"),
            hovertemplate="%{y:,.2f}",
        )

        if show_price.lower() == "true":
            # Get funding rate data timestamps
            price_data = glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(price_data["date"]).dt.strftime(
                "%Y-%m-%d"
            )
            price_data = price_data.set_index("date")

            # Add secondary Y axis for price
            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338",
                    color="#ffffff",
                )
            )

            # Add price line
            figure.add_scatter(
                x=price_data.index,
                y=price_data["price"],
                mode="lines",
                name="Price",
                line=dict(color="#F7931A"),
                yaxis="y2",
                hovertemplate="%{y:,.2f}",
            )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/lth_net_change")
async def get_lth_net_change(asset: str = "btc", show_price: str = "False"):
    try:
        data = glassnode_service.get_lth_net_change(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Ratio", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                showlegend=False,  # Removed legend
            )
        )

        # Adding single line with conditional color styling for positive/negative values
        figure.add_scatter(
            x=data.index,
            y=data["lth_net_change"],
            mode="lines",
            name="LTH Net Change",
            line=dict(color="green"),  # Base color (use for positive/initial values)
            hovertemplate="%{y}",
        )

        # Adding red for negative values by creating a secondary overlay with NaNs for positive values
        data_red = data["lth_net_change"].where(data["lth_net_change"] < 0, None)
        figure.add_scatter(
            x=data.index,
            y=data_red,
            mode="lines",
            line=dict(color="red"),
            hovertemplate="%{y}",
        )


        if show_price.lower() == "true":
            # Get funding rate data timestamps
            price_data = glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(price_data["date"]).dt.strftime(
                "%Y-%m-%d"
            )
            price_data = price_data.set_index("date")

            # Add secondary Y axis for price
            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338",
                    color="#ffffff",
                )
            )

            # Add price line
            figure.add_scatter(
                x=price_data.index,
                y=price_data["price"],
                mode="lines",
                name="Price",
                line=dict(color="#F7931A"),
                yaxis="y2",
                hovertemplate="%{y:,.2f}",
            )
            
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/historical_google_trends")
async def get_historical_google_trends(search_term: str):

    try:
        data = google_trends_service.get_historical_search_trends(search_term)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Ratio", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data[search_term], mode="lines", line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/correlation")
async def get_correlation(coin_id1: str, coin_id2: str):
    try:
        data = coingecko_service.get_correlation(coin_id1, coin_id2)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Correlation", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["correlation"],
            mode="lines",
            line=dict(color="#00b0f0"),
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/velo_futures_products")
async def get_velo_futures_products():
    data = velo_service.get_futures_products()
    return data.to_dict(orient="records")

@router.get("/velo_spot_products")
async def get_velo_spot_products():
    data = velo_service.get_spot_products()
    return data.to_dict(orient="records")

@router.get("/velo_options_products")
async def get_velo_options_products():
    data = velo_service.get_options_products()
    return data.to_dict(orient="records")

@router.get("/oi_weighted_funding_rates")
async def get_velo_oi_weighted_funding_rates(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.oi_weighted_funding_rate(coin, begin, resolution)
        data = data.set_index("time")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="OI Weighted Funding Rate", gridcolor="#2f3338", color="#ffffff"),
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        # Add bar chart for funding rate
        figure.add_bar(
            x=data.index,
            y=data["oi_weighted_funding_rate_annualized"],
            name="OI Weighted Funding Rate",
            marker_color=['rgba(0,255,0,0.3)' if x >= 0 else 'rgba(255,0,0,0.3)' 
                        for x in data["oi_weighted_funding_rate_annualized"]]
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#F7931A"),
            yaxis="y2"
        )

        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            )
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/exchange_funding_rates")
async def get_velo_funding_rates(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    data = velo_service.funding_rates(coin, begin, resolution)
    data = data.set_index("time")

    figure = go.Figure(
        layout=dict(
            xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
            yaxis=dict(title="Funding Rate", gridcolor="#2f3338", color="#ffffff"),
            margin=dict(b=0, l=0, r=0, t=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
        )
    )

    # Define colors for each exchange
    colors = {
        'binance-futures': '#F3BA2F',  # Binance yellow
        'bybit': '#4982D4',           # Bybit blue
        'okex-swap': '#BB81F6',       # OKX purple
        'hyperliquid': '#50D2C1'      # HL Green
    }

    # Plot line for each exchange
    for exchange in data['exchange'].unique():
        exchange_data = data[data['exchange'] == exchange]
        figure.add_scatter(
            x=exchange_data.index,
            y=exchange_data["annualized_funding_rate"],
            mode="lines",
            name=exchange,
            line=dict(color=colors[exchange])
        )

    return json.loads(figure.to_json())

@router.get("/long_liquidations")
async def get_velo_long_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        # Group by time to aggregate across exchanges
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum'
        }).reset_index()
        data = data.set_index("time")

        figure = go.Figure()

        # Add bar chart for liquidations
        figure.add_bar(
            x=data.index,
            y=data["buy_liquidations_dollar_volume"],
            name="Long Liquidations",
            marker_color="rgba(255,0,0,0.5)"
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#F7931A"),
            yaxis="y2"
        )

        figure.update_layout(
            xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
            yaxis=dict(title="Long Liquidations", gridcolor="#2f3338", color="#ffffff"),
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            margin=dict(b=0, l=0, r=0, t=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            hovermode='x unified'
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/short_liquidations")
async def get_velo_short_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        data = data.rename(columns={"time": "date"})
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Short Liquidations", gridcolor="#2f3338", color="#ffffff"), 
                margin=dict(b=0, l=0, r=0, t=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines", 
            name="Price",
            line=dict(color="#ffffff"),
            yaxis="y2"
    )
        
        figure.add_bar(
            x=data.index,
            y=data["sell_liquidations_dollar_volume"],
            name="Short Liquidations",
            marker=dict(color="#ff0000")
        )

        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            hovermode='x unified',
            title=f"{coin} Short Liquidations"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/net_liquidations")
async def get_velo_net_liquidations(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.liquidations(coin, begin, resolution)
        
        # Group by time to aggregate across exchanges
        data = data.groupby('time').agg({
            'close_price': 'mean',
            'buy_liquidations_dollar_volume': 'sum',
            'sell_liquidations_dollar_volume': 'sum'
        }).reset_index()
        
        # Calculate net liquidations
        data['net_liquidations'] = data['buy_liquidations_dollar_volume'] - data['sell_liquidations_dollar_volume']
        data = data.set_index("time")

        figure = go.Figure()

        # Add bar chart for net liquidations with conditional colors
        figure.add_bar(
            x=data.index,
            y=data["net_liquidations"],
            name="Net Liquidations",
            marker_color=['rgba(0,255,0,0.5)' if x >= 0 else 'rgba(255,0,0,0.5)' 
                        for x in data["net_liquidations"]]
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["close_price"],
            mode="lines",
            name="Price",
            line=dict(color="#F7931A"),
            yaxis="y2"
        )

        figure.update_layout(
            xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
            yaxis=dict(title="Net Liquidations ($)", gridcolor="#2f3338", color="#ffffff"),
            yaxis2=dict(
                title="Price ($)",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            margin=dict(b=0, l=0, r=0, t=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=True,
            hovermode='x unified',
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/open_interest")
async def get_velo_open_interest(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    try:
        data = velo_service.open_interest(coin, begin, resolution)
        
        # Group by time and exchange to get stacked data
        oi_data = data.groupby(['time', 'exchange'])['dollar_open_interest_close'].sum().reset_index()
        price_data = data.groupby('time')['close_price'].mean().reset_index()
        
        figure = go.Figure()

        # Define colors for each exchange
        colors = {
            'binance-futures': '#F3BA2F',  # Binance yellow
            'bybit': '#4982D4',           # Bybit blue
            'okex-swap': '#BB81F6',       # OKX purple
            'hyperliquid': '#50D2C1'      # HL Green
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
                    line=dict(color=colors[exchange])
                )
            )

        # Add price line on secondary axis
        figure.add_trace(
            go.Scatter(
                x=price_data['time'],
                y=price_data['close_price'],
                name="Price",
                line=dict(color="#ffffff"),
                yaxis="y2"
            )
        )

        # Update layout
        figure.update_layout(
            xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
            yaxis=dict(title="Open Interest", gridcolor="#2f3338", color="#ffffff"),
            yaxis2=dict(
                title="Price",
                overlaying="y",
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            ),
            margin=dict(b=0, l=0, r=0, t=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            showlegend=True,
            hovermode='x unified',
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/aave_lending_rate")
async def get_aave_lending_rate(
    pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"liquidityRate_avg": "lending_rate"}, inplace=True)
        data = data[["date", "lending_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Aave Lending Rate", gridcolor="#2f3338", color="#ffffff"
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lending_rate"],
            mode="lines",
            line=dict(color="#00b0f0"),
        )

        return json.loads(figure.to_json())

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aave_utilization_rate")
async def get_aave_utilization_rate(
    pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"utilizationRate_avg": "utilization_rate"}, inplace=True)
        data = data[["date", "utilization_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Aave Utilization Rate", gridcolor="#2f3338", color="#ffffff"
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["utilization_rate"],
            mode="lines",
            line=dict(color="#00b0f0"),
        )

        return json.loads(figure.to_json())

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aave_borrow_rate")
async def get_aave_borrow_rate(
    pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1",
):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"variableBorrowRate_avg": "borrow_rate"}, inplace=True)
        data = data[["date", "borrow_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Aave Borrow Rate", gridcolor="#2f3338", color="#ffffff"
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["borrow_rate"],
            mode="lines",
            line=dict(color="#00b0f0"),
        )

        return json.loads(figure.to_json())

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aave_pools")
async def get_aave_pools():
    return AAVE_POOLS



@router.get("/coinbase_app_store_rank")
async def get_coinbase_app_store_rank_route():
    try:
        data = await telegram_service.get_coinbase_app_store_rank()

        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Rank (Inverted)",
                    gridcolor="#2f3338",
                    color="#ffffff",
                    autorange="reversed"  # Invert y-axis
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["rank"], mode="lines", line=dict(color="#034AF6")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/coinbase_wallet_app_store_rank")
async def get_coinbase_wallet_app_store_rank_route():
    try:
        data = await telegram_service.get_coinbase_wallet_app_store_rank()

        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Rank (Inverted)",
                    gridcolor="#2f3338",
                    color="#ffffff",
                    autorange="reversed"  # Invert y-axis
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["rank"], mode="lines", line=dict(color="#82a7ff")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/phantom_wallet_app_store_rank")
async def get_phantom_wallet_app_store_rank_route():
    try:
        data = await telegram_service.get_phantom_wallet_app_store_rank()

        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(
                    title="Rank (Inverted)",
                    gridcolor="#2f3338",
                    color="#ffffff",
                    autorange="reversed"  # Invert y-axis
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["rank"], mode="lines", line=dict(color="#9382DE")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/glassnode_price")
async def get_glassnode_price(asset: str = "btc"):
    try:
        data = glassnode_service.get_price(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=dict(
                xaxis=dict(title="Date", gridcolor="#2f3338", color="#ffffff"),
                yaxis=dict(title="Price", gridcolor="#2f3338", color="#ffffff"),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(b=0, l=0, r=0, t=0),
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
            )
        )

        figure.add_scatter(
            x=data.index, y=data["price"], mode="lines", line=dict(color="#00b0f0")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
