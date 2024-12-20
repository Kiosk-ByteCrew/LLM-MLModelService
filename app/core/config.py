from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str
    PORT: int
    HOST: str
    OPENAI_API_KEY: str


settings = Settings()
