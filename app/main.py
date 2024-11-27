from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import get_settings
from app.api.udf_routes import router as udf_router
from app.api.general_routes import general_router
from app.api.aave_routes import aave_router
from app.api.ccdata_routes import ccdata_router
from app.api.coingecko_routes import coingecko_router
from app.api.geckoterminal_routes import geckoterminal_router
from app.api.glassnode_routes import glassnode_router
from app.api.google_trends_routes import google_trends_router
from app.api.microstrategy_routes import microstrategy_router
from app.api.telegram_routes import telegram_router
from app.api.velo_routes import velo_router

settings = get_settings()
app = FastAPI(
    title="OpenBB Terminal Pro Backend",
    description="API for cryptocurrency market analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    udf_router,
    prefix="/udf",  
    tags=["UDF"]
)

app.include_router(
    general_router,
    prefix="",
    tags=["General"]
)

app.include_router(
    aave_router,
    prefix="/aave",
    tags=["Aave"]
)

app.include_router(
    ccdata_router,
    prefix="/ccdata",
    tags=["CCData"]
)

app.include_router(
    coingecko_router,
    prefix="/coingecko",
    tags=["CoinGecko"]
)

app.include_router(
    geckoterminal_router,
    prefix="/geckoterminal",
    tags=["GeckoTerminal"]
)

app.include_router(
    glassnode_router,
    prefix="/glassnode",
    tags=["Glassnode"]
)

app.include_router(
    google_trends_router,
    prefix="/google_trends",
    tags=["Google Trends"]
)

app.include_router(
    microstrategy_router,
    prefix="/microstrategy",
    tags=["Microstrategy"]
)

app.include_router(
    telegram_router,
    prefix="/telegram",
    tags=["Telegram"]
)

app.include_router(
    velo_router,
    prefix="/velo",
    tags=["Velo"]
)

@app.get("/")
async def root():
    return {"message": "OpenBB Terminal Pro Backend is running"} 