from ..models.Auth import Auth
from ..repositories.auth_repository import login_user

def login(user: Auth):
    return login_user(user)