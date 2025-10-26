from fastapi import APIRouter
from ..models.Auth import Auth
from ..services.auth_service import login_service

router = APIRouter()

@router.post("/login", tags=["auth"])
def login(user: Auth):
    return login_service(user)
