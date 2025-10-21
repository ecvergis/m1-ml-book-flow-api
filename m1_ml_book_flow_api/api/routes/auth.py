from fastapi import APIRouter, HTTPException, status
from m1_ml_book_flow_api.core.security.security import create_access_token
from ..models.Auth import Auth
from ..services.auth_service import login

router = APIRouter()

@router.post("/login")
def login(user: Auth):
    userLogged = login(user)
    if not userLogged:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    else:
        token = create_access_token({"sub": userLogged.username})
        return {"access_token": token, "token_type": "bearer"}