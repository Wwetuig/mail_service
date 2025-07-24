'''модуль конфигурации'''
from pydantic.v1 import BaseSettings

from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    redis_url: str = os.getenv("REDIS_URL")
    smtp_server: str = os.getenv("SMTP_SERVER")
    smtp_port: int = os.getenv("SMTP_PORT")
    smtp_user: str = os.getenv("SMTP_USER")
    smtp_password: str = os.getenv("SMTP_PASSWORD")
    from_email: str = os.getenv("FROM_EMAIL")

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'

settings = Settings()