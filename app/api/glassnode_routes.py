from fastapi import APIRouter, HTTPException
from app.services.glassnode_service import GlassnodeService
from app.assets.base_chart_layout import create_base_layout
import plotly.graph_objects as go
import pandas as pd
import json

glassnode_router = APIRouter()
glassnode_service = GlassnodeService()

@glassnode_router.get("/lth_supply")
async def get_lth_supply(asset: str = "btc", show_price: str = "False"):
    try:
        data = await glassnode_service.get_lth_supply(asset)
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
            price_data = await glassnode_service.get_price(asset)
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

@glassnode_router.get("/lth_net_change")
async def get_lth_net_change(asset: str = "btc", show_price: str = "False"):
    try:
        data = await glassnode_service.get_lth_net_change(asset)
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
            price_data = await glassnode_service.get_price(asset)
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


@glassnode_router.get("/price")
async def get_glassnode_price(asset: str = "btc"):
    try:
        data = await glassnode_service.get_price(asset)
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
    
@glassnode_router.get("/mvrv_zscore")
async def get_mvrv_zscore(asset: str = "btc"):
    try:
        data = await glassnode_service.mvrv_zscore(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="MVRV Z-Score",
                y_dtype=".2f"   
            )
        )

        # Add shaded areas
        figure.add_hrect(
            y0=0, y1=-1,
            fillcolor="green", opacity=0.2,
            layer="below", line_width=0
        )
        figure.add_hrect(
            y0=6.5, y1=10,
            fillcolor="red", opacity=0.2,
            layer="below", line_width=0
        )

        # Add main MVRV Z-Score line
        figure.add_scatter(
            x=data.index,
            y=data["mvrv_zscore"],
            mode="lines",
            name="MVRV Z-Score",
            line=dict(color="#00b0f0")
        )
        
        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  
@glassnode_router.get("/lth_nupl")
async def get_lth_nupl(asset: str = "btc"):
    try:
        # Fetch and process data
        data = await glassnode_service.lth_nupl(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")
        #TODO: implement with highcharts bc plotly cant color the lines

        def assign_color(value):
            if 0 <= value < 0.25:
                return "orange"
            elif 0.25 <= value < 0.5:
                return "yellow"
            elif 0.5 <= value < 0.75:
                return "green"
            elif value >= 0.75:
                return "blue"
            return "gray"

        # Apply color assignment
        data["color"] = data["lth_nupl"].apply(assign_color)

        # Create figure layout
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="LTH NUPL",
                y_dtype=".4f"
            )
        )

        # Update layout to hide legend
        figure.update_layout(showlegend=False)

        # Create a scatter trace for each color segment
        unique_colors = data['color'].unique()
        for color in unique_colors:
            mask = data['color'] == color
            figure.add_scatter(
                x=data[mask].index,
                y=data[mask]['lth_nupl'],
                mode='lines',
                line=dict(color=color, width=2),
                hovertemplate='Value: %{y:.4f}<br>Color: ' + color + '<extra></extra>',
                showlegend=False
            )

        return json.loads(figure.to_json())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
