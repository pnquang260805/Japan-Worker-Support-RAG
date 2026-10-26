import os

from fastapi import FastAPI

from common.dependencies import get_sqlite_service
from controllers import file_controller, lm_controller, ingest_controller, user_controller
from contextlib import asynccontextmanager

from services.seed import seed_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    sqlite = get_sqlite_service()          # tạo engine + bảng
    with sqlite.SessionLocal() as db:
        seed_admin(
            db,
            email=os.environ["ADMIN_EMAIL"],
            password=os.environ["ADMIN_PASSWORD"],
        )
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(file_controller.router)
app.include_router(lm_controller.router)
app.include_router(ingest_controller.router)
app.include_router(user_controller.router)
