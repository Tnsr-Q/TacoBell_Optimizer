## backend/app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NEO4J_BOLT_URL: str = "bolt://neo4j:7687"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "dev-secret"
    USE_DB: bool = False  # switch to True once Neo4j is wired

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()


