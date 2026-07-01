from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:root@localhost:5432/ragenet"
    secret_key: str = "change-this-to-a-long-random-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cloudflare_account_id: str = ""
    cloudflare_r2_access_key_id: str = ""
    cloudflare_r2_secret_access_key: str = ""
    cloudflare_r2_bucket_name: str = ""
    cloudflare_r2_public_url: str = ""
    aws_region: str = "ap-south-1"
    ses_source_email: str = ""
    sqs_queue_url: str = ""

    model_config = {"env_prefix": ""}


settings = Settings()
