import os
from pydantic import IPvAnyAddress, PostgresDsn, EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки для FastAPI
    host: IPvAnyAddress = "127.0.0.1"
    port: int = 8001
    secret: str  # openssl rand -hex 32
    postgres_url: PostgresDsn
    token_lifetime: int = 15
    system_username: str = 'admin'
    system_pwd: str = 'admin'
    system_email: EmailStr = '9788831467@mail.ru'
    domain: str
    static_url: str = ""

    # Настройки для RabbitMQ
    rmq_host: str = os.getenv("RMQ_HOST", "127.0.0.1")
    rmq_port: int = int(os.getenv("RMQ_PORT", str(5672)))
    rmq_user: str = os.getenv("RMQ_USER", "guest")
    rmq_password: str = os.getenv("RMQ_PASSWORD", "guest")
    mq_routing_key: str = os.getenv("MQ_ROUTING_KEY", "news")

    class Config:
        env_file = '.env'

# Создание экземпляра настроек
Config = Settings()