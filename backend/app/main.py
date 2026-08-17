from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.db.init_db import init_db
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # 2. Pre-seed initial project data if table is empty
    async with AsyncSessionLocal() as session:
        await init_db(session)
        
    yield
    
    # 3. Clean up database connections on shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Set up CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}.",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "api_v1": settings.API_V1_STR
    }
