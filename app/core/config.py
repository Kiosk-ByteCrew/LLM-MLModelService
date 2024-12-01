from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE_NAME: str
    PORT: int
    HOST: str

settings = Settings()