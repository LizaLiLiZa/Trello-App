from pathlib import Path
from pydantic import IPvAnyAddress, PostgresDsn, EmailStr, BaseModel
from pydantic_settings import BaseSettings

class AuthJWT(BaseModel):
    private_key_path: Path = Path("core/services/auth/secret/private_key.pem")
    public_key_path: Path = Path("core/services/auth/secret/public_key.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 95


class Settings(BaseSettings):
    host: IPvAnyAddress = '0.0.0.0'
    port: int = 8002
    secret: str  # openssl rand -hex 32
    postgres_url: PostgresDsn
    token_lifetime: int = 15
    system_username: str = 'admin'
    system_pwd: str = 'admin'
    system_email: EmailStr = '9788831467@mail.ru'
    domain: str
    static_url: str = ""
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        env_file = '.env'



Config = Settings()