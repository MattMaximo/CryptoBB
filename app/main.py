from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import get_settings, check_api_key_exists
from app.core.registry import (
    add_template, 
    WIDGETS, 
    TEMPLATES
)
from app.routes.aave_routes import aave_router
from app.routes.btc_matrix_routes import btc_matrix_router
from app.routes.ccdata_routes import ccdata_router
from app.routes.coingecko_routes import coingecko_router
from app.routes.geckoterminal_routes import geckoterminal_router
from app.routes.glassnode_routes import glassnode_router
from app.routes.google_trends_routes import google_trends_router
from app.routes.microstrategy_routes import microstrategy_router
from app.routes.velo_routes import velo_router
from app.routes.virtuals_routes import virtuals_router
from app.core.session_manager import SessionManager
from fastapi.responses import HTMLResponse
from pathlib import Path

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: No need to create session here as it's created on first use
    yield
    # Shutdown: Clean up the session
    await SessionManager().close_session()

app = FastAPI(
    title="CryptoBB - Crypto Backend for OpenBB Workspace",
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

@app.get("/")
async def root():
    html_path = Path(__file__).parent / "core" / "landing.html"
    with open(html_path) as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Loading widgets and templates

print(f"\n\nLoading data into OpenBB workspace...\n")

if check_api_key_exists("CCDATA_API_KEY"):
    app.include_router(
        ccdata_router,
        prefix="/ccdata",
    )
    add_template("ccdata")

if check_api_key_exists("COINGECKO_API_KEY"):
    app.include_router(
        coingecko_router,
        prefix="/coingecko",
    )
    app.include_router(
        geckoterminal_router,
        prefix="/geckoterminal",
    )

    add_template("coingecko")

if check_api_key_exists("GLASSNODE_API_KEY"):
    app.include_router(
        glassnode_router,
        prefix="/glassnode",
    )
    add_template("glassnode")

if check_api_key_exists("VELO_API_KEY"):
    app.include_router(
        velo_router,
        prefix="/velo",
    )
    add_template("velodata")


app.include_router(
    google_trends_router,
    prefix="/google-trends",
)

add_template("google_trends")

app.include_router(
    microstrategy_router,
    prefix="/microstrategy",
)

app.include_router(
    aave_router,
    prefix="/aave",
)

app.include_router(
    btc_matrix_router,
    prefix="/btc-matrix",
)
add_template("btc_matrix")

app.include_router(
    virtuals_router,
    prefix="/virtuals",
)

print(f"\nLoading done.\n")

@app.get("/widgets.json")
async def get_widgets():
    return WIDGETS

# Loading custom templates

if check_api_key_exists(
    [
        "VELO_API_KEY",
        "GLASSNODE_API_KEY",
        "COINGECKO_API_KEY",
        "CCDATA_API_KEY"
    ],
    verbose=False
):
    add_template("matt_backend")

@app.get("/templates.json")
async def get_templates():
    return list(TEMPLATES.values())
