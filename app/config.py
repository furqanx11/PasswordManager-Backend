from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv("DATABASE_URL")

class Settings(BaseSettings):
    DATABASE_URL:str = db_url

    class Config:
        env_file = ".env"


settings = Settings()
