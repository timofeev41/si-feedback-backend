from typing import Annotated, Self

from fastapi.params import Depends
from loguru import logger
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as BaseSession

from src.config import Config


class SessionClass(BaseSession):
    def __enter__(self) -> Self:
        print("starting session 2")
        self.begin()
        return self

    def __exit__(self, *exceptions):  # sourcery skip: raise-specific-error
        try:
            if any(exceptions):
                self.rollback()
            else:
                try:
                    self.commit()
                except Exception as e:
                    logger.critical("failed to commit transaction.")
                    self.rollback()
                    raise Exception from e
        finally:
            super().__exit__(*exceptions)
            SyncSession.remove()


class _Database:
    def __init__(self):
        self.sync_engine = create_engine(
            str(Config.postgres_dsn),
            future=True,
            connect_args={"connect_timeout": 60},
            poolclass=NullPool,
        )

        self.sync_session_factory = sessionmaker(
            self.sync_engine,
            autobegin=False,
            autoflush=False,
            expire_on_commit=False,
            class_=SessionClass,
        )


Database = _Database()
SyncSession = scoped_session(Database.sync_session_factory)


class StartedSession(Depends):
    """Starts postgres transaction and commits it afterward."""

    def __init__(self, *args, **kwargs):
        super().__init__(self.__call__)

    @staticmethod
    def depends() -> type[SessionClass]:
        return Annotated[type[SessionClass], StartedSession()]

    async def __call__(self) -> SyncSession:
        with SyncSession() as session:
            yield session
