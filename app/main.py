from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import get_settings, check_api_key_exists
from app.api.base_routes import base_router
from app.api.aave_routes import aave_router
from app.api.ai_agent_routes import ai_agents_router
from app.api.btc_matrix_routes import btc_matrix_router
from app.api.ccdata_routes import ccdata_router
from app.api.coingecko_routes import coingecko_router
from app.api.daos_fun_routes import daos_fun_router
from app.api.geckoterminal_routes import geckoterminal_router
from app.api.glassnode_routes import glassnode_router
from app.api.google_trends_routes import google_trends_router
from app.api.microstrategy_routes import microstrategy_router
from app.api.screener_routes import screener_router
from app.api.ta_routes import ta_router
from app.api.velo_routes import velo_router
from app.api.vvaifu_routes import vvaifu_router
from app.api.virtuals_routes import virtuals_router
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

print(f"\n\nLoading data into OpenBB workspace...\n")

app.include_router(
    base_router,
    prefix="",
)

if check_api_key_exists("CCDATA_API_KEY"):
    app.include_router(
        ccdata_router,
        prefix="/ccdata",
    )
    app.include_router(
        ta_router,
        prefix="/ta",
    )

if check_api_key_exists("COINGECKO_API_KEY_1"):
    app.include_router(
        coingecko_router,
        prefix="/coingecko",
    )

if check_api_key_exists("GLASSNODE_API_KEY"):
    app.include_router(
        glassnode_router,
        prefix="/glassnode",
    )

if check_api_key_exists("VELO_API_KEY"):
    app.include_router(
        velo_router,
        prefix="/velo",
    )

app.include_router(
    daos_fun_router,
    prefix="/daos_fun",
)

app.include_router(
    geckoterminal_router,
    prefix="/geckoterminal",
)


app.include_router(
    google_trends_router,
    prefix="/google-trends",
)

app.include_router(
    microstrategy_router,
    prefix="/microstrategy",
)

app.include_router(
    screener_router,
    prefix="/screener",
)

app.include_router(
    aave_router,
    prefix="/aave",
)

app.include_router(
    ai_agents_router,
    prefix="/ai-agents",
)

app.include_router(
    btc_matrix_router,
    prefix="/btc-matrix",
)

app.include_router(
    vvaifu_router,
    prefix="/vvaifu",
)

app.include_router(
    virtuals_router,
    prefix="/virtuals",
)

print(f"\nLoading done.\n")