from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.models.session import SyncSession
from src.routers import auth, feedback_session, users, feedback


# @asynccontextmanager
# async def lifespan(fastapi_app: FastAPI):
#     """XXX: Nothing there now..."""

app = FastAPI()

app.include_router(auth.router)
app.include_router(feedback_session.router)
app.include_router(users.router)
app.include_router(feedback.router)
