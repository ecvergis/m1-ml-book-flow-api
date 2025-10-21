from pydantic.v1 import BaseModel

class Auth(BaseModel):
    username: str
    password: str