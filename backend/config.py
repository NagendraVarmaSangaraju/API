from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL = "sqlite:///./app.db"


settings = Settings()
