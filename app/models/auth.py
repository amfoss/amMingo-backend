from pydantic import BaseModel

class RegisterUser(BaseModel):
    email: str
    username: str
    name: str
    password: str

class UserDetails(BaseModel):
    email: str
    username: str
    name: str