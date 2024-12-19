# %%
from fastapi import APIRouter, HTTPException
from app.services.btc_matrix_service import BTCMatrixService
from app.assets.charts.base_matrix_layout import get_matrix_figure
import pandas as pd
import json
import plotly.express as px

btc_matrix_router = APIRouter()
btc_matrix_service = BTCMatrixService()

def _format_btc_amount(value_str):
    """Convert BTC amount strings to K/M format"""
    value = int(value_str.replace(',', ''))
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    return f"{value/1_000:.0f}K"


@btc_matrix_router.get("/reserve-dollars")
async def get_btc_reserve_matrix(return_fig: bool = True):
    reserve_matrix = btc_matrix_service.generate_reserve_matrix()
    reserve_matrix.index = [_format_btc_amount(idx) for idx in reserve_matrix.index]
    reserve_matrix.columns = [col.strip('%') for col in reserve_matrix.columns]
    
    fig_reserves = get_matrix_figure(reserve_matrix, y_label="BTC Reserve Amount", hover_label="BTC ($T)")
    if return_fig:
        return json.loads(fig_reserves.to_json())

    else:
        return reserve_matrix

@btc_matrix_router.get("/reserve-pct")
async def get_btc_reserve_matrix_pct(return_fig: bool = True):
    pct_matrix = btc_matrix_service.generate_pct_matrix(
        starting_debt=37_000_000_000_000,
        debt_cagr=0.05
    )
    
    pct_matrix.index = [_format_btc_amount(idx) for idx in pct_matrix.index]
    pct_matrix.columns = [col.strip('%') for col in pct_matrix.columns]
    
    fig_pct = get_matrix_figure(pct_matrix, y_label="BTC Reserve Amount", hover_label=r"% of Debt")
    if return_fig:
        return json.loads(fig_pct.to_json())
    else:
        return pct_matrix

# %%
