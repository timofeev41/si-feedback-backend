from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    postgres_dsn: str = Field("postgresql+psycopg2://postgres:postgres@localhost:5432/feedback", validate_default=False)
    secret_key: str = Field("SOMEKEY", validate_default=False)
    algorithm: str = Field("HS256", validate_default=False)
    access_token_expire_minutes: int = Field(0, validate_default=False)


Config = _Config()
