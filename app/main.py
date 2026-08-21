from fastapi import FastAPI

from app.config.settings import get_settings
from app.database.init_db import init_database
from app.router.routes.user_router import router as user_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
)

app.include_router(user_router)


@app.on_event("startup")
def startup() -> None:
    """Handles application startup events.

    Initializes database tables and necessary schema configurations prior to accepting requests.
    """
    init_database()
