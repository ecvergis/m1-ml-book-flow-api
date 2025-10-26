from ..models.Auth import Auth
from ..repositories.auth_repository import login_user
from m1_ml_book_flow_api.core.security.security import create_access_token
from fastapi import HTTPException, status

def login_service(user: Auth):
    userLogged = login_user(user)
    if not userLogged:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    token = create_access_token({"sub": userLogged.username})
    return {"access_token": token, "token_type": "bearer"}
