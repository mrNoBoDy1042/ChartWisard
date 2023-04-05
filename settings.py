from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ChartWizard for Metabase"
    version: int = 1
    