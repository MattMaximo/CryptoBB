from fastapi import APIRouter, HTTPException
from app.core.widgets import WIDGETS
from app.services.coingecko_service import CoinGeckoService

coingecko_service = CoinGeckoService()
screener_router = APIRouter()

@screener_router.get("/watchlist")
async def get_watchlist():
    coin_ids = "bitcoin,ethereum,ripple,solana,tron,avalanche-2,chainlink,stellar,sui,uniswap,eigenlayer,aave,celestia,hyperliquid,dogwifcoin,injective-protocol,jupiter-exchange-solana,virtual-protocol,helium,raydium,apecoin,pendle,grass,goatseus-maximus,echelon-prime,drift-protocol,zerebro,cetus-protocol,kamino,aixbt,banana-gun,morpho,near,the-open-network,researchcoin,vitadao,blub,navi,ai16z,wormhole,tensor,vaderai-by-virtuals,arbitrum,optimism,hivemapper"
    data = await coingecko_service.get_coin_list_market_data(coin_ids)
    data.fillna("", inplace=True)
    data = data[['market_cap_rank', 'name', 'symbol', 'current_price', 'total_volume', 'market_cap',
        'fully_diluted_valuation', 'price_change_percentage_1h_in_currency',
        'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency',
        'price_change_percentage_14d_in_currency', 'price_change_percentage_30d_in_currency',
        'price_change_percentage_200d_in_currency', 'price_change_percentage_1y_in_currency',
        'circulating_supply', 'total_supply', 'max_supply', 'ath', 'ath_date', 'atl', 'atl_date']]
    
    data = data.rename(columns={
        'market_cap_rank': 'rank',
        'current_price': 'price', 
        'total_volume': 'volume',
        'fully_diluted_valuation': 'fdv',
        'price_change_percentage_1h_in_currency': '1h_pct_change',
        'price_change_percentage_24h_in_currency': '24h_pct_change',
        'price_change_percentage_7d_in_currency': '7d_pct_change',
        'price_change_percentage_14d_in_currency': '14d_pct_change',
        'price_change_percentage_30d_in_currency': '30d_pct_change',
        'price_change_percentage_200d_in_currency': '200d_pct_change',
        'price_change_percentage_1y_in_currency': '1y_pct_change'
    })

    data['symbol'] = data['symbol'].str.upper()
    return data.to_dict(orient="records")

