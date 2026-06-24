from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:root@localhost:5432/ragenet"
    secret_key: str = "change-this-to-a-long-random-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = {"env_prefix": ""}


settings = Settings()
