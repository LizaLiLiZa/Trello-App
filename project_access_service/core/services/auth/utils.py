import jwt
import datetime
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def encode_jwt(
        payload: dict,
        key: str = Config.auth_jwt.private_key_path.read_text(encoding='utf-8'),
        algorithm: str = Config.auth_jwt.algorithm,
        expire_timedelta: datetime.timedelta | None = None,
        expire_minutes: int = Config.auth_jwt.access_token_expire_minutes):

    to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        key, 
        algorithm=algorithm)
    return encoded

def decode_jwt(
        token: str | bytes,
        public_key: str = Config.auth_jwt.public_key_path.read_text(encoding='utf-8'),
        algorithm: str = Config.auth_jwt.algorithm):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])

    role = decoded.get("role")
    sub = decoded.get("sub")

    return decoded, role, sub

def decode_roles(
        token: str | bytes,
        public_key: str = Config.auth_jwt.public_key_path.read_text(encoding='utf-8'),
        algorithm: str = Config.auth_jwt.algorithm):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])

        role = decoded.get("role")
        print(role)

        return role
    except Exception as exp:
        raise HTTPException(status_code=422, detail="Срок токена истек.") from exp

def decode_sub(
        token: str | bytes,
        public_key: str = Config.auth_jwt.public_key_path.read_text(encoding='utf-8'),
        algorithm: str = Config.auth_jwt.algorithm):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])

        sub = decoded.get("sub")

        return sub
    except Exception as exp:
        raise HTTPException(status_code=422, detail="Срок токена истек.") from exp

def decode_id_project(
        token: str | bytes,
        public_key: str = Config.auth_jwt.public_key_path.read_text(encoding='utf-8'),
        algorithm: str = Config.auth_jwt.algorithm):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])

        id_project = decoded.get("id_project")

        return id_project
    except Exception as exp:
        raise HTTPException(status_code=422, detail="Срок токена истек.") from exp
