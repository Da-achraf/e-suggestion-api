import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from typing import Annotated

from schemas import User
from schemas.auth import TokenCreationSettings, TokenVerificationSettings
from core.config import JWTSettings, SettingsDep
from db.dependencies import SessionDep
from db.repositories import UserRepositoryDep


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_token(sett: TokenCreationSettings):
    expire = datetime.now(timezone.utc) + sett.expiry
    sett.to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        sett.to_encode,
        sett.key,
        algorithm=sett.algorithm
    )
    return encoded_jwt


def create_reset_password_token(email: str, settings: JWTSettings):
    to_encode = {
        "sub": email
    }

    sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.FORGET_PWD_SECRET,
        expiry=timedelta(minutes=int(settings.FORGET_PWD_EXPIRE_MINUTES)),
        algorithm=settings.ALGORITHM
    )

    return create_token(sett=sett)


async def verify_token(sett: TokenVerificationSettings):
    try:
        payload = jwt.decode(
            token=sett.token,
            key=sett.key,
            algorithms=[sett.algorithm]
        )

        user_id = payload.get("user_id")
        
        return user_id
    except InvalidTokenError:
        raise
    
    
# Generate access and refresh tokens
def generate_tokens(user: User, settings: JWTSettings):
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token_expires = timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    
    to_encode = {
        "sub": user.email,
        'roles': [role.name for role in user.roles],
        'user_id': user.id
    }
    
    access_token_sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.SECRET,
        expiry=access_token_expires,
        algorithm=settings.ALGORITHM
    )
    
    refresh_token_sett = TokenCreationSettings(
        to_encode=to_encode,
        key=settings.REFRESH_SECRET,
        expiry=refresh_token_expires,
        algorithm=settings.ALGORITHM
    )
    

    access_token = create_token(access_token_sett)
    refresh_token = create_token(refresh_token_sett)

    return [access_token, refresh_token]


async def get_current_user(
    settings: SettingsDep,
    db: SessionDep,
    user_repository: UserRepositoryDep,
    token: str = Depends(oauth2_scheme)
):
    sett = TokenVerificationSettings(
        token=token,
        key=settings.JWT.SECRET,
        algorithm=settings.JWT.ALGORITHM
    )
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = await verify_token(sett)
    if user_id is None:
        raise credentials_exception
    
    user = user_repository.find_by_id(model_id=user_id, db=db)
    if user is None:
        raise credentials_exception
    
    return user

def get_authenticated_user(
        login_req: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repository: UserRepositoryDep,
        db: SessionDep
):
    found_user = user_repository.find_by_username_or_email(
        email=login_req.username,
        db=db
    )

    if not found_user:
        return False
    if not verify_password(login_req.password, found_user.hashed_password):
        return False
    return User.model_validate(found_user)




def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password)