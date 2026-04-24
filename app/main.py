from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.session import close_db, init_db


# Startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup and shutdown"""
    # STARTUP
    print("Initializing database...")
    await init_db()
    print("Database ready")

    yield

    # SHUTDOWN
    print("Closing connections...")
    await close_db()
    print("Goodbye!")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready Todo API",
    docs_url="/docs" if settings.DEBUG else None,  # Hide docs in prod!
    redoc_url=None,  # Hide ReDoc
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["monitoring"])
async def health_check():
    return {"status": "healthy"}
    return {"status": "healthy"}
