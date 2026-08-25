from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import get_settings
from app.database.init_db import init_database
from app.exceptions.handlers import register_exception_handlers
from app.router.routes.user_router import router as user_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events.

    Initializes database tables before the application starts serving requests.
    """

    init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(user_router)
