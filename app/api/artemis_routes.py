from fastapi import APIRouter, HTTPException
from app.services.artemis_service import ArtemisService
from app.services.coingecko_service import CoinGeckoService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
from app.assets.queries.altcoin_season import altcoin_season_query
from app.assets.queries.category_market_cap import get_category_market_cap_query
from app.core.widget_decorator import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

artemis_router = APIRouter()
artemis_service = ArtemisService()
coingecko_service = CoinGeckoService()

@artemis_router.get("/altcoin-season-index")
@register_widget({
    "name": "Altcoin Season Index",
    "description": (
        "Altcoin Season Index calculates the number of coins in the top 50 "
        "that outperform Bitcoin over a 90 day period."
    ),
    "category": "crypto",
    "defaultViz": "chart",
    "endpoint": "artemis/altcoin-season-index",
    "gridData": {"w": 20, "h": 9},
    "source": "Artemis",
    "params": [
        {
            "paramName": "price_coin",
            "value": "bitcoin",
            "label": "Compare Price",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_altcoin_season_index(
    price_coin: str = 'bitcoin', 
    theme: str = "dark"
):

    try:
        altcoin_season_data = await artemis_service.execute_query(altcoin_season_query)
        altcoin_season_data['DATE'] = pd.to_datetime(altcoin_season_data['DATE'])
        altcoin_season_data['ALT_SEASON'] = altcoin_season_data['ALT_SEASON'].astype(float) / 100

        price_coin = price_coin.lower()
        btc_data = await coingecko_service.get_market_data(price_coin)
        btc_data = btc_data[['date', f'{price_coin}_price']]
        
        # Calculate forward-looking returns
        btc_data['1m_return'] = btc_data[f'{price_coin}_price'].shift(-30).div(btc_data[f'{price_coin}_price']).sub(1) * 100
        btc_data['3m_return'] = btc_data[f'{price_coin}_price'].shift(-90).div(btc_data[f'{price_coin}_price']).sub(1) * 100
        btc_data['6m_return'] = btc_data[f'{price_coin}_price'].shift(-180).div(btc_data[f'{price_coin}_price']).sub(1) * 100
        
        # Inner join on date column to only keep matching dates
        merged_data = altcoin_season_data.merge(btc_data, left_on='DATE', right_on='date', how='left')
        
        # Get chart colors based on theme
        colors = get_chart_colors(theme)
        
        fig = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Altcoin Season Index",
                y_dtype=".0%",
                theme=theme
            )
        )

        # Update layout to include secondary y-axis and shared hover mode
        fig.update_layout(
            yaxis2=dict(
                title=dict(
                    text=f"{price_coin.title()} Price (USD)",
                    font=dict(color=colors['secondary'])
                ),
                overlaying="y",
                side="right",
                showgrid=False,
                tickformat=",d"  # Format as integer with commas
            ),
            hovermode='x unified',  # This makes all traces share the same hover
            hoverlabel=dict(
                namelength=-1  # Show full trace names
            ),
            xaxis=dict(
                hoverformat="%m-%d-%Y"  # Format the hover date
            )
        )

        # Add Altcoin Season Index with hover template
        fig.add_trace(
            go.Scatter(
                x=merged_data['DATE'],
                y=merged_data['ALT_SEASON'],
                mode='lines',
                name='Altcoin Season Index',
                line=dict(color=colors['main_line']),
                hovertemplate="<b>Index</b>: %{y:.0%}<br><extra></extra>"
            )
        )

        # Add Bitcoin price with hover template including returns
        fig.add_trace(
            go.Scatter(
                x=merged_data['DATE'],
                y=merged_data[f'{price_coin}_price'],
                mode='lines',
                name=f'{price_coin.title()}',
                yaxis='y2',
                line=dict(color=colors['secondary']),
                hovertemplate=(
                    "<b>Price</b>: $%{y:,.0f}<br>" +
                    "%{customdata[3]}"  # Use a pre-formatted string for returns
                ) + "<extra></extra>",
                customdata=merged_data.apply(
                    lambda row: [
                        row['1m_return'],
                        row['3m_return'],
                        row['6m_return'],
                        # Create formatted return string, showing only non-NaN values
                        "<br>".join([
                            f"<b>1M Return</b>: {row['1m_return']:.1f}%" if pd.notna(row['1m_return']) else "",
                            f"<b>3M Return</b>: {row['3m_return']:.1f}%" if pd.notna(row['3m_return']) else "",
                            f"<b>6M Return</b>: {row['6m_return']:.1f}%" if pd.notna(row['6m_return']) else ""
                        ]).strip("<br>")
                    ],
                    axis=1
                ).values
            )
        )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(fig, theme=theme)
        
        # Convert figure to JSON with the config
        figure_json = fig.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    


@artemis_router.get("/ai-testing")
#TODO: fix
async def ai_testing():
    data = await coingecko_service.get_coin_list_market_data(category="virtuals-protocol-ecosystem")
    data.fillna(0, inplace=True)
    ids = data['id'].tolist()
    
    # Get the dynamic query with the ids list
    dynamic_query = get_category_market_cap_query(ids)
    category_data = await artemis_service.execute_query(dynamic_query)

    return category_data.to_dict(orient="records")