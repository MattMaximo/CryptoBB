from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.udf_routes import router as udf_router
from app.core.settings import get_settings

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

app.include_router(router)

app.include_router(
    udf_router,
    prefix="/udf",  
    tags=["UDF"]
)

@app.get("/")
async def root():
    return {"message": "OpenBB Terminal Pro Backend is running"} 