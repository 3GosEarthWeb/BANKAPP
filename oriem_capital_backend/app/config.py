from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
from pydantic import Field, SecretStr, field_validator
import json


class Settings(BaseSettings):
    # ========= 🌍 Environment ==========
    APP_ENV: str = "development"

    # ========= 🛢️ Database ==========
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/oriemdb"
    POOL_DATABASE_URL: Optional[str] = None
    DIRECT_DATABASE_URL: Optional[str] = None

    # ========= 🔐 Auth / Security ==========
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ========= 🌐 CORS ==========
    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            try:
                # Try parsing as JSON list
                return json.loads(value)
            except json.JSONDecodeError:
                # Fall back to comma-separated string
                return [v.strip() for v in value.split(",") if v.strip()]
        return value

    # ========= 🗂️ Static Files ==========
    STATIC_DIR: str = "app/static"
    UPLOAD_DIR: str = "app/static/uploads"

    # ========= 📧 Email ==========
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: SecretStr
    SMTP_SENDER: str
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    # ========= 🔑 Supabase ==========
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # ========= 📦 Misc ==========
    PROJECT_NAME: str = "ORiem Capital API"
    VERSION: str = "1.0.0"
    REDOC_URL: str = "/redoc"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
