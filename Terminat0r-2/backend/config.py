import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str = "sqlite:///./terminat0r2.db"
    gemini_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""
    ai_provider: str = "groq"

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
