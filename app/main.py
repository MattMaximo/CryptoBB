from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import get_settings
from app.api.base_routes import base_router
from app.api.artemis_routes import artemis_router
from app.api.aave_routes import aave_router
from app.api.ccdata_routes import ccdata_router
from app.api.coingecko_routes import coingecko_router
from app.api.geckoterminal_routes import geckoterminal_router
from app.api.glassnode_routes import glassnode_router
from app.api.google_trends_routes import google_trends_router
from app.api.microstrategy_routes import microstrategy_router
from app.api.screener_routes import screener_router
from app.api.telegram_routes import telegram_router
from app.api.ta_routes import ta_router
from app.api.velo_routes import velo_router
from app.core.session_manager import SessionManager

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: No need to create session here as it's created on first use
    yield
    # Shutdown: Clean up the session
    await SessionManager().close_session()

app = FastAPI(
    title="OpenBB Terminal Pro Backend",
    description="API for cryptocurrency market analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    base_router,
    prefix="",
    tags=["Base Routes no prefix"]
)

app.include_router(
    artemis_router,
    prefix="/artemis",
    tags=["Artemis"]
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
    screener_router,
    prefix="/screener",
    tags=["Screener"]
)

app.include_router(
    telegram_router,
    prefix="/telegram",
    tags=["Telegram"]
)

app.include_router(
    ta_router,
    prefix="/ta",
    tags=["Technical Analysis"]
)

app.include_router(
    velo_router,
    prefix="/velo",
    tags=["Velo"]
)

@app.get("/")
async def root():
    return {"message": "OpenBB Terminal Pro Backend is running"}

