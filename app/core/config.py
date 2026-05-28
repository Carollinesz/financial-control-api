from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="latin-1", extra="ignore")

    PROJECT_NAME: str = "financial-api"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    PROD: bool = False

    DATABASE_URL: str
    MIGRATION_DATABASE_URL: str
    
    DEBUG: bool = False


settings = Settings()
