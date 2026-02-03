from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App config; reads from env and .env."""

    db_name: str = "tenders.db"
    db_path: str = "data/tenders.db"
    base_url: str = "http://127.0.0.1:8000"
    max_items: int = 10

    class Config:
        env_file = ".env"


_settings: Settings | None = None


def get_settings() -> Settings:
    """Cached settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings