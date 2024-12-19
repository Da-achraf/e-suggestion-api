from typing import Dict
from pydantic import BaseModel
from datetime import timedelta


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    refresh_token: str
    token_type: str
    
class TokenCreationSettings(BaseModel):
    to_encode: Dict
    key: str
    expiry: timedelta
    algorithm: str

    class Config:
        arbitrary_types_allowed = True

class TokenVerificationSettings(BaseModel):
    token: str
    key: str
    algorithm: str

class UserLoginRequest(BaseModel):
    email: str
    password: str
    
class UserRegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    account_status: bool = False
    
class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str
    confirm_password: str
    
class ForgetPasswordRequest(BaseModel):
    email: str

class ResetPasswordTokenVerificationRequest(BaseModel):
    token: str