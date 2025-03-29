# %%
from fastapi import APIRouter, HTTPException
from app.services.btc_matrix_service import BTCMatrixService
from app.assets.charts.base_matrix_layout import get_matrix_figure
from app.assets.charts.plotly_config import apply_config_to_figure
from app.core.registry import register_widget
import pandas as pd
import json


btc_matrix_router = APIRouter()
btc_matrix_service = BTCMatrixService()


def _format_btc_amount(value_str):
    """Convert BTC amount strings to K/M format"""
    value = int(value_str.replace(',', ''))
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    return f"{value/1_000:.0f}K"


def _update_figure_for_theme(fig, theme="dark"):
    """Update figure colors based on theme"""
    # Get text color based on theme
    text_color = '#333333' if theme == "light" else '#FFFFFF'
    
    # Update text colors for axes
    fig.update_layout(
        font=dict(color=text_color),
        xaxis=dict(color=text_color),
        yaxis=dict(color=text_color)
    )
    
    # Update text color for matrix values
    cell_text_color = "black" if theme == "light" else "white"
    fig.update_traces(textfont=dict(color=cell_text_color))
    
    return fig


@btc_matrix_router.get("/reserve-dollars")
@register_widget({
    "name": "BTC Reserve Matrix (USD)",
    "description": (
        "Matrix showing Bitcoin reserves of countries and companies in USD"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "btc-matrix/reserve-dollars",
    "widgetId": "btc-matrix/reserve-dollars",
    "gridData": {"w": 20, "h": 9},
    "source": "BTCMatrix",
    "data": {"chart": {"type": "heatmap"}},
})
async def get_btc_reserve_matrix(return_fig: bool = True, theme: str = "dark"):
    reserve_matrix = btc_matrix_service.generate_reserve_matrix()
    reserve_matrix.index = [
        _format_btc_amount(idx) for idx in reserve_matrix.index
    ]
    reserve_matrix.columns = [
        col.strip('%') for col in reserve_matrix.columns
    ]
    
    fig_reserves = get_matrix_figure(
        reserve_matrix, 
        y_label="BTC Reserve Amount", 
        hover_label="BTC ($T)"
    )

    # Apply theme configuration
    fig_reserves = apply_config_to_figure(
        fig_reserves, 
        theme=theme
    )
    
    if return_fig:
        return json.loads(fig_reserves.to_json())
    else:
        return reserve_matrix


@btc_matrix_router.get("/reserve-pct")
@register_widget({
    "name": "BTC Reserve Matrix (%)",
    "description": (
        "Matrix showing Bitcoin reserves of countries and companies as a "
        "percentage of their total reserves"
    ),
    "category": "crypto",
    "type": "chart",
    "endpoint": "btc-matrix/reserve-pct",
    "widgetId": "btc-matrix/reserve-pct",
    "gridData": {"w": 20, "h": 9},
    "source": "BTCMatrix",
    "data": {"chart": {"type": "heatmap"}},
})
async def get_btc_reserve_matrix_pct(
    return_fig: bool = True, 
    theme: str = "dark"
):
    pct_matrix = btc_matrix_service.generate_pct_matrix(
        starting_debt=37_000_000_000_000,
        debt_cagr=0.05
    )
    
    pct_matrix.index = [
        _format_btc_amount(idx) for idx in pct_matrix.index
    ]
    pct_matrix.columns = [
        col.strip('%') for col in pct_matrix.columns
    ]
    
    figure = get_matrix_figure(
        pct_matrix, 
        y_label="BTC Reserve Amount", 
        hover_label=r"% of Debt"
    )
    
    # Apply theme configuration
    figure = apply_config_to_figure(
        figure, 
        theme=theme
    )
    
    if return_fig:
        return json.loads(figure.to_json())
    else:
        return pct_matrix

# %%
