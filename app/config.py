from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_USER_PWD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()