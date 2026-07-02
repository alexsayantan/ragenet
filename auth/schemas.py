from pydantic import BaseModel
from datetime import datetime


class UserSignup(BaseModel):
    email: str
    username: str
    password: str


class UserSignin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    username: str


class UserDetail(BaseModel):
    uuid: str
    username: str
    created_at: datetime


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
