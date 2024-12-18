from sqlmodel import SQLModel, Field
from typing import Optional

class UserRoleLink(SQLModel, table=True):
    __tablename__ = "users_roles"
    role_id: Optional[int] = Field(
        default=None, 
        foreign_key="roles.id", 
        primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, 
        foreign_key="users.id", 
        primary_key=True
    )