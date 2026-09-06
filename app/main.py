from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import get_settings
from app.database.init_db import init_database
from app.exceptions.handlers import register_exception_handlers
from app.router.routes.auth_router import router as auth_router
from app.router.routes.user_router import router as user_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Handles application startup and shutdown lifecycle events.

    Initializes database tables prior to accepting incoming HTTP requests and cleans up resources on shutdown.

    Args:
        app (FastAPI): The main FastAPI application instance.

    Yields:
        None: Yields control back to the application to handle requests.
    """

    init_database()
    yield


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(user_router)
app.include_router(auth_router)
