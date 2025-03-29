# %%
from fastapi import APIRouter, HTTPException
from app.services.coingecko_service import CoinGeckoService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.queries.category_market_cap import get_category_market_cap_query
import plotly.graph_objects as go
import pandas as pd
import json

ai_agents_router = APIRouter()
coingecko_service = CoinGeckoService()

@ai_agents_router.get("/ai-agent-category-market-caps")
async def get_ai_agent_category_market_cap():
    ai_categories = {
        'ai-agents': [],
        'ai-meme-coins': [],
        'ai-applications': [],
        'ai-agent-launchpad': [],
        #'artificial-intelligence': []
    }

    # First loop - get coin IDs for each category
    for category in ai_categories:
        try:
            data = await coingecko_service.get_coin_list_market_data(category=category)
            ai_categories[category] = data['id'].tolist()
        except Exception as e:
            print(f"Error getting coin list for category {category}: {e}")

    # Combine all dataframes
    combined_df = pd.concat(dfs, axis=1)
    combined_df = combined_df.fillna(0)  # Fill NaN values with 0
    
    # Create the figure
    fig = go.Figure(
        layout=create_base_layout(
            x_title="Date",
            y_title="Market Cap (USD)",
        )
    )

    # Color palette for different categories
    colors = {
        'ai-agents': '#1f77b4',
        'ai-meme-coins': '#ff7f0e',
        'ai-applications': '#2ca02c',
        'ai-agent-launchpad': '#d62728',
        'artificial-intelligence': '#9467bd'
    }

    # Add a trace for each category
    for category in ai_categories:
        fig.add_trace(
            go.Scatter(
                x=combined_df.index,
                y=combined_df[category],
                mode='lines',
                name=category.replace('-', ' ').title(),
                line=dict(color=colors[category]),
                hovertemplate="<b>%{x|%Y-%m-%d}</b><br>" +
                            f"{category.replace('-', ' ').title()}: $%{{y:,.0f}}<extra></extra>"
            )
        )

    # Update layout for better visualization
    fig.update_layout(
        yaxis=dict(
            #type='log',  # Use log scale for better visibility of all categories
            tickformat="$,.0f",  # Format y-axis ticks as currency
        ),
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    try:
        return json.loads(fig.to_json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")
