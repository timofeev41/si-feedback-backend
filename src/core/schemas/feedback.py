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


class TotalFeedbackSummarySchema(BaseSchema):
    total: str


class FeedbackFormSchema(BaseSchema):
    fields: list[dict]
    header: str
