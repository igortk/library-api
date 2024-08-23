from pydantic_settings import BaseSettings, SettingsConfigDict


class HttpSettings(BaseSettings):
    port: int = 5000

    model_config = SettingsConfigDict(env_file=".env", env_prefix="http_")


class PostgresSettings(BaseSettings):
    url: str = "postgresql://postgres:password@localhost:5432/postgres522525"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="pg_")
