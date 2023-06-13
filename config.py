from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'ChartWizard'
    version: int = 1
    openai_api_key: str
    cookie_secret_key: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    root_path = Path(__file__).parent.absolute()


settings = Settings()