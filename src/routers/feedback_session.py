import uuid

from fastapi import APIRouter, HTTPException, Body

from src.core.dependencies.auth import CurrentUser
from src.core.handlers.feedback import handle_single_active_session
from src.core.models.feedback_session import FeedbackSession
from src.core.models.session import StartedSession
from src.core.schemas.feedback import FeedbackSessionSchema, TotalFeedbackSummarySchema
from src.core.utils.gpt_api import get_total_feedback_summary

router = APIRouter(
    prefix="/feedback-sessions",
    tags=["Feedback Sessions"],
    dependencies=[StartedSession()],
)


@router.get("/{user_id}", response_model=list[FeedbackSessionSchema])
async def get_feedback_sessions(user_id: int, current_user: CurrentUser):
    return FeedbackSession.select(FeedbackSession.author_id == user_id)


@router.get("/total-summary/{user_id}", response_model=TotalFeedbackSummarySchema)
async def get_total_summary(user_id: int, current_user: CurrentUser):
    return TotalFeedbackSummarySchema(total=get_total_feedback_summary(user_id))


@router.post("/", response_model=FeedbackSessionSchema)
async def create_feedback_session(
    current_user: CurrentUser,
    title: str = Body(..., embed=True),
):
    with handle_single_active_session():
        if FeedbackSession.select(
            FeedbackSession.is_active == True,
            FeedbackSession.author_id == current_user.id,
        ):
            raise ValueError("Only one active test session allowed")
        return FeedbackSession.insert(
            id=uuid.uuid4(),
            author_id=current_user.id,
            is_active=True,
            ts_deactivated=None,
            title=title,
        )


@router.patch("/{session_id}", response_model=FeedbackSessionSchema)
async def end_feedback_session(session_id: uuid.UUID, current_user: CurrentUser):
    try:
        if session := FeedbackSession.one(FeedbackSession.id == session_id):
            session.deactivate(current_user.id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Session not found or already ended") from e
