from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class JWTSettings(BaseSettings):
    SECRET: str
    REFRESH_SECRET: str
    FORGET_PWD_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    FORGET_PWD_EXPIRE_MINUTES: int
    ALGORITHM: str
    
class DatabaseSettings(BaseSettings):
    HOST: str
    USER: str
    PASSWORD: str
    NAME: str
    URL: str

class Settings(BaseSettings):
    PROJECT_TITLE: str
    MODE: str
    APP_HOST: str
    APP_PORT: int
    APP_WORKERS: int
    DB: DatabaseSettings
    JWT: JWTSettings

@lru_cache
def get_settings() -> Settings:
    # Extract JWT and DB settings from the environment variables
    jwt_env_values = {k[len('JWT_'):]: v for k, v in os.environ.items() if k.startswith('JWT_')}
    db_env_values = {k[len('DB_'):]: v for k, v in os.environ.items() if k.startswith('DB_')}

    # Create instances of the settings classes
    jwt_settings = JWTSettings(**jwt_env_values)
    db_settings = DatabaseSettings(**db_env_values)

    # Return the Settings instance
    settings = Settings(
        PROJECT_TITLE=os.getenv('PROJECT_TITLE'),
        MODE=os.getenv('MODE'),
        APP_HOST=os.getenv('APP_HOST'),
        APP_PORT=int(os.getenv('APP_PORT')),
        APP_WORKERS=int(os.getenv('APP_WORKERS')),
        DB=db_settings,
        JWT=jwt_settings
    )
    
    return settings

SettingsDep = Annotated[Settings, Depends(get_settings)]
