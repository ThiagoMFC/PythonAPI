from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_USER_PWD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_MINUTES: int

    model_config = ConfigDict(
        env_file = ".env"
    )

    #class Config:
        #env_file = ".env"

settings = Settings()