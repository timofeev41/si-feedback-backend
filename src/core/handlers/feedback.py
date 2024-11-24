from fastapi import HTTPException, status

from contextlib import contextmanager


@contextmanager
def handle_already_sent_feedback():
    try:
        yield
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]) from e


@contextmanager
def handle_single_active_session():
    try:
        yield
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0]) from e
