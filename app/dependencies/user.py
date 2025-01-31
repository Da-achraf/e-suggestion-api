from fastapi import HTTPException, status, Depends
from typing import Annotated

from app.db.repositories import UserRepositoryDep
from app.db.dependencies import SessionDep
from app.core.security import get_password_hash
from app.db.models import UserCreate, UserInDb


def get_user_to_save(
    user: UserCreate,
    user_repository: UserRepositoryDep,
    db: SessionDep
):
    found_user = user_repository.find_by_username_or_email(
        email=user.email,
        db=db
    )
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    user_data = user.model_dump()
    
    # Hash the password
    user_data['hashed_password'] = get_password_hash(user.password)
    return UserInDb(**user_data)

UserToSaveDep = Annotated[UserCreate, Depends(get_user_to_save)]