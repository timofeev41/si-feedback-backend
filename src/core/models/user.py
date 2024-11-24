import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if typing.TYPE_CHECKING:
    from .feedback_session import FeedbackSession


class User(BaseModel):
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=True)
    position: Mapped[str] = mapped_column(nullable=True)
    company: Mapped[str] = mapped_column(nullable=True)

    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)

    feedback_sessions: Mapped["FeedbackSession"] = relationship(back_populates="author", uselist=True)
