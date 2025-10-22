from m1_ml_book_flow_api.api.models.Auth import Auth

USERS_DB = {"admin": "password123"}
# USERS_DB = {
#     "username": "admin",
#     "password": "password123"
# }

def login_user(user: Auth):
    if user.username not in USERS_DB or USERS_DB[user.username] != user.password:
        return None
    else:
        return user
