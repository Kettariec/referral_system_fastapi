from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DATABASE_URL: Optional[str] = None
    ALGORITHM: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    FRONTEND_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()

settings.DATABASE_URL = (f"postgresql+asyncpg://{settings.DB_USER}:"
                         f"{settings.DB_PASS}@{settings.DB_HOST}:"
                         f"{settings.DB_PORT}/{settings.DB_NAME}")
