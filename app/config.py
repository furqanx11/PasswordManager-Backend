from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://furqan:1234@localhost:5432/password_manager"

settings = Settings()
