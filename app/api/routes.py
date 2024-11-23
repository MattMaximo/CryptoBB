from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.coingecko_service import CoinGeckoService
from app.services.glassnode_service import GlassnodeService
from app.services.google_trends_service import GoogleTrendsService
from app.services.velo_service import VeloService
from app.services.aave_service import AaveService
from app.services.telegram_service import TelegramService
from app.services.microstrategy_service import MicrostrategyService
from app.services.ccdata_service import CCDataService
from app.services.geckoterminal_service import GeckoTerminalService
from app.core.widgets import WIDGETS
from app.assets.aave_pools import AAVE_POOLS
from app.assets.base_chart_layout import create_base_layout
from app.assets.ai_agent_mapping import ai_agent_mapping
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
microstrategy_service = MicrostrategyService()
ccdata_service = CCDataService()
geckoterminal_service = GeckoTerminalService()


@router.get("/widgets.json")
async def get_widgets():
    return WIDGETS


@router.get("/coingecko_coin_list")
async def get_coin_list(include_platform: str = "true", status: str = "active"):
    symbols_list = coingecko_service.get_coin_list(include_platform, status)
    return symbols_list.to_dict(orient="records")


@router.get("/coingecko_price")
async def get_market_data(coin_id: str):
    try:
        data = coingecko_service.get_market_data(coin_id)
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Dominance (%)"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["dominance"] * 100,
            mode="lines",
            line=dict(color="#00b0f0"),
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
            line=dict(color="#00b0f0"),
            hovertemplate="%{y:.2f}"  # Format hover as decimal
        )
        figure.update_yaxes(tickformat=".2f")  # Override tick format to show decimals

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/lth_supply")
async def get_lth_supply(asset: str = "btc", show_price: str = "False"):
    try:
        data = glassnode_service.get_lth_supply(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="LTH Supply"
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
            price_data = glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(price_data["date"]).dt.strftime("%Y-%m-%d")
            price_data = price_data.set_index("date")

            # Add secondary Y axis for price
            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338",
                    color="#ffffff"
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Net Change"
            )
        )

        # Update layout to hide legend for this specific chart
        figure.update_layout(showlegend=False)

        # Adding single line with conditional color styling
        figure.add_scatter(
            x=data.index,
            y=data["lth_net_change"],
            mode="lines",
            name="LTH Net Change",
            line=dict(color="green"),
            hovertemplate="%{y}"
        )

        # Adding red for negative values
        data_red = data["lth_net_change"].where(data["lth_net_change"] < 0, None)
        figure.add_scatter(
            x=data.index,
            y=data_red,
            mode="lines",
            line=dict(color="red"),
            hoverinfo="skip"
        )

        if show_price.lower() == "true":
            price_data = glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(price_data["date"]).dt.strftime("%Y-%m-%d")
            price_data = price_data.set_index("date")

            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338",
                    color="#ffffff"
                )
            )

            figure.add_scatter(
                x=price_data.index,
                y=price_data["price"],
                mode="lines",
                name="Price",
                line=dict(color="#F7931A"),
                yaxis="y2",
                hovertemplate="%{y:,.2f}"
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Search Interest"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data[search_term],
            mode="lines",
            line=dict(color="#00b0f0")
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Correlation"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["correlation"],
            mode="lines",
            line=dict(color="#00b0f0")
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


@router.get("/exchange_funding_rates")
async def get_velo_funding_rates(coin: str = "BTC", begin: str = None, resolution: str = "1d"):
    data = velo_service.funding_rates(coin, begin, resolution)
    data = data.set_index("time")

    figure = go.Figure(
        layout=create_base_layout(
            x_title="Date",
            y_title="Funding Rate"
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
            line=dict(color=colors[exchange]),
            hovertemplate="%{y:.2%}"
        )
    # Update y-axis to show percentage format
    figure.update_layout(
        yaxis=dict(
            tickformat=".0%",  # Format as percentage with no decimals
            gridcolor="#2f3338",
            color="#ffffff"
        )
    )

    return json.loads(figure.to_json())

@router.get("/long_liquidations")
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

@router.get("/short_liquidations")
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

@router.get("/net_liquidations")
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

@router.get("/open_interest")
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




@router.get("/aave_lending_rate")
async def get_aave_lending_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"liquidityRate_avg": "lending_rate"}, inplace=True)
        data = data[["date", "lending_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Lending Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lending_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aave_utilization_rate")
async def get_aave_utilization_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"utilizationRate_avg": "utilization_rate"}, inplace=True)
        data = data[["date", "utilization_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Utilization Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["utilization_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aave_borrow_rate")
async def get_aave_borrow_rate(pool: str = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e1"):
    try:
        data = aave_service.get_lending_pool_history(pool)
        data.rename(columns={"variableBorrowRate_avg": "borrow_rate"}, inplace=True)
        data = data[["date", "borrow_rate"]]
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Borrow Rate"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["borrow_rate"],
            mode="lines",
            line=dict(color="#00b0f0")
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#034AF6")
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#82a7ff")
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Rank"
            )
        )

        # Update yaxis to be inverted
        figure.update_layout(
            yaxis=dict(
                autorange="reversed",
                gridcolor="#2f3338",
                color="#ffffff",
                title="Rank"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["rank"],
            mode="lines",
            line=dict(color="#9382DE")
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
            layout=create_base_layout(
                x_title="Date",
                y_title="Price"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["price"],
            mode="lines",
            line=dict(color="#00b0f0")
        )
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/microstrategy_premium")
async def get_microstrategy_premium():
    try:
        data = microstrategy_service.get_prices()
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Nav Premium"
            )
        )

        # Add secondary Y axis for price
        figure.update_layout(
            yaxis2=dict(
                title="Price",
                overlaying="y", 
                side="right",
                gridcolor="#2f3338",
                color="#ffffff"
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["nav_premium"],
            mode="lines",
            name="NAV Premium",
            line=dict(color="#00b0f0"),
            hovertemplate="%{y:.2f}"
        )

        # Add price line on secondary y-axis
        figure.add_scatter(
            x=data.index,
            y=data["btc_price"],
            mode="lines", 
            name="BTC Price",
            line=dict(color="#F7931A"),
            yaxis="y2",
            hovertemplate="%{y:,.2f}"
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/microstrategy_info")
async def get_microstrategy_info():
    try:
        data = microstrategy_service.get_treasury_data()
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/exchange_price_deltas")
async def get_exchange_price_deltas():
    try:
        data = ccdata_service.get_delta_data()
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
    
@router.get("/ai_agents_market_data")
async def get_ai_agents_market_data():
    try:
        data = geckoterminal_service.fetch_ai_agent_market_data(ai_agent_mapping)
        data.fillna(0, inplace=True)

        float_columns = ['price_usd', 'volume_usd', 'market_cap_usd', 'fdv_usd', 
                        'total_supply', 'total_reserve_in_usd']
        for col in float_columns:
            if col in data.columns:
                data[col] = data[col].astype(float, errors='ignore')
                
        return data.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/geckoterminal_ohlcv")
async def get_geckoterminal_ohlcv(symbol: str, timeframe: str, aggregate: int):
    try:
        pool_id = ai_agent_mapping[symbol.upper()]['pool_id']
        chain = ai_agent_mapping[symbol.upper()]['chain']
        data = geckoterminal_service.fetch_pool_ohlcv_data(pool_id, chain, timeframe, aggregate)
        data = data.set_index("timestamp")
        print(data.shape)

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
            y=data['volume'],
            name="Volume",
            yaxis="y2",
            marker_color='rgba(128,128,128,0.5)'
        )

        # Add candlestick chart second so it appears on top
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
            yaxis2=dict(
                title="Volume", 
                overlaying="y",
                side="right",
                showgrid=False
            )
        )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))