from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MASTER_DB_USER: str
    MASTER_DB_PASSWORD: str
    MASTER_DB_HOSTNAME: str
    MASTER_DB_PORT: str
    MASTER_DB_NAME: str

settings = Settings()