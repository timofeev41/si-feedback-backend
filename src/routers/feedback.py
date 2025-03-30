from datetime import datetime
import uuid

from fastapi import APIRouter, Body, HTTPException

from src.core.dependencies.auth import CurrentUser, AdminUser
from src.core.dependencies.feedback import FetchSession, get_feedback_session
from src.core.models.feedback_session import FeedbackResponse
from src.core.models.session import StartedSession
from src.core.schemas.feedback import FeedbackFormSchema, PerformanceAnalyticsSchema

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

mock_performance_summary = """
Over the past quarter, the team member demonstrated consistent performance across key metrics. 
They completed 92% of assigned Jira tickets on time and contributed to 3 major features. 
Code quality has improved, with a 25% reduction in code review rework. 
There is a noticeable increase in cross-functional collaboration, with active involvement in 2 cross-team initiatives.
"""

mock_performance_analytics = [
    {
        "name": "tickets_completed_on_time",
        "label": "Tickets Completed On Time",
        "value": "92%"
    },
    {
        "name": "features_delivered",
        "label": "Features Delivered",
        "value": "3"
    },
    {
        "name": "code_review_rework_reduction",
        "label": "Code Review Rework Reduction",
        "value": "25%"
    },
]

@router.post("/{session_id}")
async def submit_feedback(session_id: uuid.UUID, user: CurrentUser, data: dict = Body(..., embed=True)):
    session = await get_feedback_session(session_id)
    try:
        return FeedbackResponse.insert(
            session_id=session.id,
            author=user,
            data=data,
            ts_created=datetime.now(),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@router.get("/{session_id}", response_model=FeedbackFormSchema)
async def get_feedback_form(session: FetchSession, __: CurrentUser):
    # TODO: Real feedback form customization using tables and admin panel!
    return FeedbackFormSchema(fields=mock_feedback_form, header=session.get_title())

@router.get("/{session_id}/analytics", response_model=PerformanceAnalyticsSchema)
async def get_performance_analytics(session: FetchSession, __: CurrentUser):
    # TODO: Real performance analytics
    # Performance analytics processing flow:
    # - admin uploads json with raw performance data from Jira or some other tracker
    # - backend exposes endpoint for analytics upload
    # - the uploaded json is stored in a table for raw analytics data. One to Many relationship with User  (use intermediate table to connect User and analytics)
    # - backend has a cronjob that checks for new raw analytics records every N period
    # - if new raw analytics records are found, they are passed to LLM along with a specific prompt and user information
    # - LLM produces summary of the performance data (summarized) and a list of metrics with values (fields)
    # - the LLM output is stored in a table for processed analytics data. One to Many relationship with User  (use intermediate table to connect User and analytics)

    # when /{session_id}/analytics is called, retrieve latest record from processed performance analytics table by username of session owner
    return PerformanceAnalyticsSchema(fields=mock_performance_analytics, summarized=mock_performance_summary)

@router.get("/{session_id}/sent")
async def get_sent_feedbacks_to_session(session: FetchSession, _: AdminUser):
    """Get all feedbacks related to session, only accessible for admin accounts."""
    return session.responses
