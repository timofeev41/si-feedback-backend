import typing
import uuid
from datetime import datetime
from typing import Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from .base import BaseModel
from .user import User


class FeedbackSession(BaseModel):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False, unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    ts_deactivated: Mapped[datetime] = mapped_column(nullable=True)

    author: Mapped["User"] = relationship(back_populates="feedback_sessions")
    responses: Mapped[typing.List["FeedbackResponse"]] = relationship(back_populates="feedback_session")

    def deactivate(self, user_id: int):
        if user_id == self.author_id and self.is_active:
            self.is_active = False
            self.ts_deactivated = datetime.now()
            self.save()
            return
        raise ValueError("Wrong user or session already ended")

    def get_title(self):
        req = all((self.author.full_name, self.author.position, self.author.company))
        if req:
            return f"{self.title} for {self.author.full_name} ({self.author.position} at {self.author.company})"
        return f"{self.title} for someone (doing something somewhere), to get this filled correctly go to patch /users/"


class FeedbackResponse(BaseModel):
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("feedback_session.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    # json field with feedback
    data: Mapped[dict] = mapped_column(JSONB, nullable=False, default="{}")
    ts_created: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)

    author: Mapped["User"] = relationship()
    feedback_session: Mapped["FeedbackSession"] = relationship()

    @classmethod
    def insert(cls, **kwargs) -> Self:
        if cls.one(
            cls.author_id == kwargs.pop("author").id,
            cls.session_id == kwargs.pop("session_id"),
        ):
            raise ValueError("User already sent his feedback on this form.")
        return super().insert(**kwargs)
