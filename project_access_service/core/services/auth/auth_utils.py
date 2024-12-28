from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .utils import decode_roles
from .utils import decode_sub
from .utils import decode_id_project
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    roles = decode_roles(token)
    if not roles:
        raise HTTPException(status_code=403, detail="Roles not found in token")
    return roles

def get_current_user_sub(token: str = Depends(oauth2_scheme)):
    sub = decode_sub(token)
    if not sub:
        raise HTTPException(status_code=403, detail="sub not found in token")
    return sub

def get_current_user_id_project(token: str = Depends(oauth2_scheme)):
    id_project = decode_id_project(token)
    if not id_project:
        raise HTTPException(status_code=403, detail="id_project not found in token")
    return id_project
