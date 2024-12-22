from pydantic import IPvAnyAddress, PostgresDsn, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: IPvAnyAddress = '0.0.0.0'
    port: int = 8000
    secret: str  # openssl rand -hex 32
    postgres_url: PostgresDsn
    token_lifetime: int = 15
    system_username: str = 'admin'
    system_pwd: str = 'admin'
    system_email: EmailStr = '9788831467@mail.ru'
    domain: str
    static_url: str = ""

    class Config:
        env_file = '.env'



Config = Settings()