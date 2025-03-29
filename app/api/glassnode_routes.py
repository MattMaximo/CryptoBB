from fastapi import APIRouter, HTTPException
from app.services.glassnode_service import GlassnodeService
from app.assets.charts.base_chart_layout import create_base_layout
from app.assets.charts.plotly_config import (
    apply_config_to_figure, 
    get_chart_colors
)
from app.core.widget_decorator import register_widget
import plotly.graph_objects as go
import pandas as pd
import json

glassnode_router = APIRouter()
glassnode_service = GlassnodeService()

@glassnode_router.get("/lth-supply")
@register_widget({
    "name": "Long Term Holders Supply",
    "description": (
        "Supply of long term holders"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "glassnode/lth-supply",
    "widgetId": "glassnode/lth-supply",
    "gridData": {"w": 20, "h": 9},
    "source": "Glassnode",
    "params": [
        {
            "paramName": "asset",
            "value": "btc",
            "label": "Coin",
            "type": "text",
            "description": "Glassnode ID of the cryptocurrency",
        },
        {
            "paramName": "show_price",
            "value": "False",
            "label": "Show Price",
            "type": "text",
            "description": "Overlay price on chart",
            "options": [
                {"value": "True", "label": "True"},
                {"value": "False", "label": "False"},
            ],
        },
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_lth_supply(
    asset: str = "btc", 
    show_price: str = "False", 
    theme: str = "dark"
):
    try:
        data = await glassnode_service.get_lth_supply(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="LTH Supply",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["lth_supply"],
            mode="lines",
            name="LTH Supply",
            line=dict(color=colors['main_line']),
            hovertemplate="%{y:,.2f}",
        )

        if show_price.lower() == "true":
            price_data = await glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(
                price_data["date"]
            ).dt.strftime("%Y-%m-%d")
            price_data = price_data.set_index("date")

            # Add secondary Y axis for price
            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338" if theme == "dark" else "#dddddd",
                    color="#ffffff" if theme == "dark" else "#333333"
                )
            )

            # Add price line
            figure.add_scatter(
                x=price_data.index,
                y=price_data["price"],
                mode="lines",
                name="Price",
                line=dict(color=colors['secondary']),
                yaxis="y2",
                hovertemplate="%{y:,.2f}",
            )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@glassnode_router.get("/lth-net-change")
@register_widget({
    "name": "Long Term Holders Net Position Change",
    "description": (
        "Net position change of long term holders"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "glassnode/lth-net-change",
    "widgetId": "glassnode/lth-net-change",
    "gridData": {"w": 20, "h": 9},
    "source": "Glassnode",
    "params": [
        {
            "paramName": "asset",
            "value": "btc",
            "label": "Coin",
            "type": "text",
            "description": "Glassnode ID of the cryptocurrency",
        },
        {
            "paramName": "show_price",
            "value": "False",
            "label": "Show Price",
            "type": "text",
            "description": "Overlay price on chart",
            "options": [
                {"value": "True", "label": "True"},
                {"value": "False", "label": "False"},
            ],
        },
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_lth_net_change(
    asset: str = "btc", 
    show_price: str = "False", 
    theme: str = "dark"
):
    try:
        data = await glassnode_service.get_lth_net_change(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Net Change",
                theme=theme
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
            line=dict(color=colors['positive']),
            hovertemplate="%{y}"
        )

        # Adding red for negative values
        data_red = data["lth_net_change"].where(
            data["lth_net_change"] < 0, None
        )
        figure.add_scatter(
            x=data.index,
            y=data_red,
            mode="lines",
            line=dict(color=colors['negative']),
            hoverinfo="skip"
        )

        if show_price.lower() == "true":
            price_data = await glassnode_service.get_price(asset)
            price_data["date"] = pd.to_datetime(
                price_data["date"]
            ).dt.strftime("%Y-%m-%d")
            price_data = price_data.set_index("date")

            figure.update_layout(
                yaxis2=dict(
                    title="Price",
                    overlaying="y",
                    side="right",
                    gridcolor="#2f3338" if theme == "dark" else "#dddddd",
                    color="#ffffff" if theme == "dark" else "#333333"
                )
            )

            figure.add_scatter(
                x=price_data.index,
                y=price_data["price"],
                mode="lines",
                name="Price",
                line=dict(color=colors['secondary']),
                yaxis="y2",
                hovertemplate="%{y:,.2f}"
            )

        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@glassnode_router.get("/price")
@register_widget({
    "name": "Glassnode Price",
    "description": "Historical price data from Glassnode",
    "category": "crypto",
    "type": "chart",
    "endpoint": "glassnode/price",
    "widgetId": "glassnode/price",
    "gridData": {"w": 20, "h": 9},
    "source": "Glassnode",
    "params": [
        {
            "paramName": "asset",
            "value": "btc",
            "label": "Coin",
            "type": "text",
            "description": "Glassnode ID of the cryptocurrency",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_glassnode_price(asset: str = "btc", theme: str = "dark"):
    try:
        data = await glassnode_service.get_price(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="Price",
                theme=theme
            )
        )

        figure.add_scatter(
            x=data.index,
            y=data["price"],
            mode="lines",
            line=dict(color=colors['main_line'])
        )

        # Apply the standard configuration to the figure with theme
        figure, _ = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
    
        return figure_dict

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@glassnode_router.get("/mvrv-zscore")
@register_widget({
    "name": "MVRV Z-Score",
    "description": (
        "Market Value to Realized Value Z-Score, a metric to assess if "
        "Bitcoin is over or undervalued"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "glassnode/mvrv-zscore",
    "widgetId": "glassnode/mvrv-zscore",
    "gridData": {"w": 20, "h": 9},
    "source": "Glassnode",
    "params": [
        {
            "paramName": "asset",
            "value": "btc",
            "label": "Coin",
            "type": "text",
            "description": "Glassnode ID of the cryptocurrency",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_mvrv_zscore(asset: str = "btc", theme: str = "dark"):
    try:
        data = await glassnode_service.mvrv_zscore(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        data = data.set_index("date")

        # Get chart colors based on theme
        colors = get_chart_colors(theme)

        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="MVRV Z-Score",
                y_dtype=".2f",
                theme=theme
            )
        )

        # Add shaded areas
        figure.add_hrect(
            y0=0, y1=-1,
            fillcolor=colors['positive'], opacity=0.2,
            layer="below", line_width=0
        )
        figure.add_hrect(
            y0=6.5, y1=10,
            fillcolor=colors['negative'], opacity=0.2,
            layer="below", line_width=0
        )

        # Add main MVRV Z-Score line
        figure.add_scatter(
            x=data.index,
            y=data["mvrv_zscore"],
            mode="lines",
            name="MVRV Z-Score",
            line=dict(color=colors['main_line'])
        )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)

        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
  
@glassnode_router.get("/lth-nupl")
@register_widget({
    "name": "Long Term Holders NUPL",
    "description": (
        "Net Unrealized Profit/Loss for long term holders"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "glassnode/lth-nupl",
    "widgetId": "glassnode/lth-nupl",
    "gridData": {"w": 20, "h": 9},
    "source": "Glassnode",
    "params": [
        {
            "paramName": "asset",
            "value": "btc",
            "label": "Coin",
            "type": "text",
            "description": "Glassnode ID of the cryptocurrency",
        }
    ],
    "data": {"chart": {"type": "line"}},
})
async def get_lth_nupl(asset: str = "btc", theme: str = "dark"):
    try:
        # Fetch and process data
        data = await glassnode_service.lth_nupl(asset)
        data["date"] = pd.to_datetime(data["date"]).dt.strftime("%Y-%m-%d")
        
        # Sort data by date to ensure chronological order
        data = data.sort_values("date")
        
        # Create a continuous index for the data
        dates = data["date"].tolist()
        lth_nupl_values = data["lth_nupl"].tolist()
        
        # Get chart colors based on theme
        colors = get_chart_colors(theme)
        
        # Define color thresholds
        color_thresholds = [
            (0.0, 0.25, colors['secondary']),  # orange equivalent
            (0.25, 0.5, colors['tertiary']),   # yellow equivalent
            (0.5, 0.75, colors['positive']),   # green
            (0.75, float('inf'), colors['neutral']),  # blue
        ]
        
        # Create figure layout
        figure = go.Figure(
            layout=create_base_layout(
                x_title="Date",
                y_title="LTH NUPL",
                y_dtype=".4f",
                theme=theme
            )
        )
        
        # Update layout to hide legend
        figure.update_layout(showlegend=False)
        
        # Create a visual break where the value crosses thresholds
        segments = []
        current_segment = {"x": [], "y": [], "color": None}
        
        # Initialize with the first point
        if lth_nupl_values:
            current_value = lth_nupl_values[0]
            for threshold_min, threshold_max, color in color_thresholds:
                if threshold_min <= current_value < threshold_max:
                    current_segment["color"] = color
                    break
            else:
                current_segment["color"] = "#777777"  # Default gray
            
            current_segment["x"].append(dates[0])
            current_segment["y"].append(current_value)
        
        # Process remaining points
        for i in range(1, len(dates)):
            current_date = dates[i]
            current_value = lth_nupl_values[i]
            
            # Determine color for current value
            current_color = "#777777"  # Default gray
            for threshold_min, threshold_max, color in color_thresholds:
                if threshold_min <= current_value < threshold_max:
                    current_color = color
                    break
            
            # If color changes, end current segment and start a new one
            if current_color != current_segment["color"]:
                # Add the current point to complete the previous segment
                current_segment["x"].append(current_date)
                current_segment["y"].append(current_value)
                
                # Save the completed segment
                segments.append(current_segment)
                
                # Start a new segment with the current point
                current_segment = {
                    "x": [current_date],
                    "y": [current_value],
                    "color": current_color
                }
            else:
                # Continue the current segment
                current_segment["x"].append(current_date)
                current_segment["y"].append(current_value)
        
        # Add the last segment if it has data
        if current_segment["x"]:
            segments.append(current_segment)
        
        # Add all segments to the figure, ensuring they connect perfectly at transition points
        for i, segment in enumerate(segments):
            figure.add_trace(
                go.Scatter(
                    x=segment["x"],
                    y=segment["y"],
                    mode='lines',
                    line=dict(color=segment["color"], width=2),
                    hovertemplate='Value: %{y:.4f}<extra></extra>',
                    showlegend=False
                )
            )
        
        # Apply the standard configuration to the figure with theme
        figure = apply_config_to_figure(figure, theme=theme)
        
        # Convert figure to JSON with the config
        figure_json = figure.to_json()
        figure_dict = json.loads(figure_json)
        
        return figure_dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
