from datetime import datetime, timedelta
import jwt

SECRET_KEY = "minha_chave_secreta_teste"
ALGORITHM = "HS256"

def create_test_token(user_id: str, expires_delta: timedelta = None):
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
