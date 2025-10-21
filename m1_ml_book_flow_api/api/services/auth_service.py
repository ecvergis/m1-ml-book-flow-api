from ..models.Auth import Auth
from ..repositories.auth_repository import login

def login(user: Auth):
    return login(user)