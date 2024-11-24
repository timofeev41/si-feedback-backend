import uuid
from datetime import datetime

from .base import BaseSchema


class FeedbackResponsesSchema(BaseSchema):
    id: int
    author_id: int
    data: dict
    ts_created: datetime


class FeedbackSessionSchema(BaseSchema):
    id: uuid.UUID
    author_id: int
    is_active: bool
    ts_deactivated: datetime | None
    responses: list[FeedbackResponsesSchema]
    title: str | None
    gpt_summary: str = 'Super good performance! There will be some text from GPT-4o mini model!!! yay so cool'


class TotalFeedbackSummarySchema(BaseSchema):
    total: str


class FeedbackFormSchema(BaseSchema):
    fields: list[dict]
    header: str
