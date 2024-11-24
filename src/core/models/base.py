import re
from typing import Self

from sqlalchemy import func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, object_session, Session

from .session import SyncSession


class BaseModel(DeclarativeBase):
    """SQLAlchemy BaseModel class."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", cls.__name__).lower()

    def dict(self) -> dict:
        return self.__dict__

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    @property
    def session(self) -> Session:
        return object_session(self) or SyncSession

    def save(self):
        session = self.session
        session.add(self)
        session.flush()
        return self

    # TODO: delete_one and delete
    def delete(self):
        self.session.delete(self)

    # TODO: insert_one and insert
    @classmethod
    def insert(cls, **kwargs) -> Self:
        return cls(**kwargs).save()

    @classmethod
    def one(cls, *filters) -> Self:
        return SyncSession.scalar(select(cls).where(*filters))

    # TODO: add options
    @classmethod
    def select(cls, *filters, offset=0, limit=None) -> list[Self]:
        expression = select(cls).where(*filters).offset(offset).limit(limit)
        return list(SyncSession.scalars(expression).unique())

    @classmethod
    async def count(cls, *filters) -> int:
        return SyncSession.scalar(select(func.count(cls.id)).where(*filters))
