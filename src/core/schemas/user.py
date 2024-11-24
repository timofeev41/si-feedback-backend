from .base import BaseSchema


class UserSchema(BaseSchema):
    username: str
    id: int
    full_name: str | None
    position: str | None
    company: str | None


class UserUpdateSchema(BaseSchema):
    full_name: str
    position: str
    company: str
