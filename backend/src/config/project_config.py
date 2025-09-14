from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str
    MAX_FILE_SIZE: int
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
