from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    CTP_PROJECT_KEY: Optional[str] = None
    CTP_CLIENT_ID: Optional[str] = None
    CTP_CLIENT_SECRET: Optional[str] = None
    CTP_AUTH_URL: str = "https://auth.europe-west1.gcp.commercetools.com"
    CTP_API_URL: str = "https://api.europe-west1.gcp.commercetools.com"
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
