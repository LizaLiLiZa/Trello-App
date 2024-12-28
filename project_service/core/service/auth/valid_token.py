import httpx
from fastapi import HTTPException, Header

async def valid_token_person(id_person:int, authorization: str = Header(None)) -> bool:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    
    # Проверяем токен на наличие "Bearer"
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]  # Извлекаем сам токен
    else:
        raise HTTPException(status_code=401, detail="Invalid token format")

    headers = {
        "Authorization": f"Bearer {token}"  # Убедитесь, что токен правильно передан
    }
    async with httpx.AsyncClient() as client:
        await client.get(f"http://127.0.0.1:8000/api/valid-token?id_person={id_person}", headers=headers)
    return token

async def valid_token_person_project(id_person:int, role: str, id_project: int, authorization: str = Header(None)) -> bool:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization token is missing")
    
    # Проверяем токен на наличие "Bearer"
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]  # Извлекаем сам токен
    else:
        raise HTTPException(status_code=401, detail="Invalid token format")

    headers = {
        "Authorization": f"Bearer {token}"  # Убедитесь, что токен правильно передан
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8002/api/valid-token?id_person={id_person}&name_role={role}&id_project={id_project}", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Token validation failed")
        data = response.json()
        return data

