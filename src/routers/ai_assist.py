from fastapi import APIRouter

from src.core.dependencies.auth import CurrentUser
from src.core.models.session import StartedSession


router = APIRouter(
    prefix='/ai-assist',
    tags=['AI Assist'],
    dependencies=[StartedSession()],
)


@router.post('/feedback')
async def assist_feedback_form_row(
    label: str, filled_value: str, user_id: str, current_user: CurrentUser
):
    return 'currently in progress'