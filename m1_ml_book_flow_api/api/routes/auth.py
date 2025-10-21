from fastapi import APIRouter, HTTPException, status
from m1_ml_book_flow_api.core.security.security import create_access_token

router = APIRouter()

USERS_DB = {"admin": "password123"}

@router.post("/login")
def login(username: str, password: str):
    if username not in USERS_DB or USERS_DB[username] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}