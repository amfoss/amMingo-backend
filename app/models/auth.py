from pydantic import BaseModel


class UserDetails(BaseModel):
    email: str
    username: str
    name: str
    code: str


class EmailLoginRequest(BaseModel):
    email: str


class EmailVerify(BaseModel):
    email: str
    otp: str
