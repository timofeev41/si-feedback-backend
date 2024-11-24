from .base import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str = "Bearer"


class AuthData(BaseSchema):
    username: str
    password: str
