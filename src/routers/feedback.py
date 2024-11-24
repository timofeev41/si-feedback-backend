from datetime import datetime

from fastapi import APIRouter, Body

from src.core.dependencies.auth import CurrentUser, AdminUser
from src.core.dependencies.feedback import FetchSession
from src.core.handlers.feedback import handle_already_sent_feedback
from src.core.models.feedback_session import FeedbackResponse
from src.core.models.session import StartedSession
from src.core.schemas.feedback import FeedbackFormSchema

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
    dependencies=[StartedSession()],
)


mock_feedback_form = [
    {
        "name": "perf_scale",
        "label": "Performance Scale",
        "type": "select",
        "options": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "required": True,
    },
    {
        "name": "perf_scale_input",
        "label": "About this person's performance",
        "type": "textarea",
        "required": True,
    },
    {
        "name": "overall_score",
        "label": "Overall Score",
        "type": "select",
        "options": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "required": True,
    },
    {
        "name": "overall_score_input",
        "label": "About this person's overall score",
        "type": "textarea",
        "required": True,
    },
]


@router.post("/{session_id}")
async def submit_feedback(fb_session: FetchSession, user: CurrentUser, data: dict = Body(..., embed=True)):
    with handle_already_sent_feedback():
        return FeedbackResponse.insert(
            session_id=fb_session.id,
            author=user,
            data=data,
            ts_created=datetime.now(),
        )


@router.get("/{session_id}", response_model=FeedbackFormSchema)
async def get_feedback_form(session: FetchSession, __: CurrentUser):
    # TODO: Real feedback form customization using tables and admin panel!
    return FeedbackFormSchema(fields=mock_feedback_form, header=session.get_title())


@router.get("/{session_id}/sent")
async def get_sent_feedbacks_to_session(session: FetchSession, _: AdminUser):
    """Get all feedbacks related to session, only accessible for admin accounts."""
    return session.responses
