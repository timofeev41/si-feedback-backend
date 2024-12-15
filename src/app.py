from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routers import auth, feedback_session, users, feedback, ai_assist


# @asynccontextmanager
# async def lifespan(fastapi_app: FastAPI):
#     """XXX: Nothing there now..."""

app = FastAPI(title='Smart Industry Feedback Service API', version='0.0.1sigma-patrick-bateman')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(feedback_session.router)
app.include_router(users.router)
app.include_router(feedback.router)
app.include_router(ai_assist.router)
