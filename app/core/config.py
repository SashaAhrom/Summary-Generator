from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "AI-Powered Online Course Summary Generator"
    database_url: str
    openai_api_key: str 
    number_of_requests: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
