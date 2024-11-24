from typing import Annotated

from fastapi import HTTPException, Depends

import uuid

from src.core.dependencies.auth import CurrentUser
from src.core.models.feedback_session import FeedbackSession


async def get_feedback_session(session_id: uuid.UUID):
    if not (session := FeedbackSession.one(FeedbackSession.id == session_id)):
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.is_active:
        raise HTTPException(status_code=400, detail="Session is closed")
    return session


FetchSession = Annotated[FeedbackSession, Depends(get_feedback_session)]
