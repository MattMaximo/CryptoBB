from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.graph_objects as go
from app.services.virtuals_service import VirtualsService
from app.services.coingecko_service import CoinGeckoService
from app.assets.queries.category_market_cap import get_category_market_cap_query
from app.assets.charts.base_chart_layout import create_base_layout
import json
virtuals_router = APIRouter()
virtuals_service = VirtualsService()
coingecko_service = CoinGeckoService()

@virtuals_router.get("/agents-data")
async def get_agents_list():
    """
    Get list of virtual agents and their data
    """
    try:
        df = await virtuals_service.get_agents_list()
        df.fillna(0, inplace=True)
        return df.to_dict(orient="records") 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    

@virtuals_router.get("/agents-market-caps")
async def get_agents_market_caps():
    """
    Get market caps of virtual agents
    """
    try:
        virtuals_agents = await coingecko_service.get_coin_list_market_data(category="virtuals-protocol-ecosystem")
        virtuals_agents.fillna(0, inplace=True)
        virtuals_agents["market_cap"] = virtuals_agents["market_cap"].astype(float)
        virtuals_agents = virtuals_agents[virtuals_agents["total_volume"] >= 500000]
        virtuals_agents = virtuals_agents[virtuals_agents["id"] != "virtual-protocol"]
        virtuals_agents_ids = virtuals_agents["id"].tolist()

        df = await coingecko_service.get_market_data(virtuals_agents_ids)
        df.fillna(0, inplace=True)
        df = df[df["date"].dt.time == pd.to_datetime("00:00:00").time()]
        df = df[["date", "market_cap", "coingecko_id"]]
        df.rename(columns={"market_cap": "market_cap_usd"}, inplace=True)

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df = df.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Market Cap (USD)"
            )
        )

        # Create a line for each coingecko_id
        for coingecko_id in df["coingecko_id"].unique():
            coin_data = df[df["coingecko_id"] == coingecko_id]
            figure.add_scatter(
                x=coin_data.index,
                y=coin_data["market_cap_usd"],
                mode="lines",
                name=coingecko_id,
                hovertemplate="$%{y:,.0f}"
            )

        return json.loads(figure.to_json())
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 