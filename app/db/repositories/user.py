from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session, select

from app.db.crud_repository import CRUDBaseRepository, get_repository
from app.db.models import UserModel, User

class UserRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(UserModel, User)
        
    def find_by_username_or_email(
            self,
            db: Session,
            email: Optional[str] = None
    ) -> Optional[User]:
        statement = select(self.model).where(
            self.model.email == email
        )
        result = db.exec(statement).first()
        return result
    
    def toggle_approve(self, db: Session, user_id: int):
        user = self.find_by_id(db, user_id)
        if not user:
            return None
        user.account_status = not user.account_status
        db.commit()
        db.refresh(user)
        return user

UserRepositoryDep = Annotated[UserRepository, Depends(get_repository(UserRepository))]