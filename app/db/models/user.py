from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, Enum
from db.models.associations import UserRoleLink
from db.models.role import Role
from db.models.bu import BU

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    hashed_password: str = Field(max_length=255)
    email: str = Field(unique=True, max_length=255)
    account_status: bool = Field(default=False)

    bu_id: Optional[int] = Field(default=None, foreign_key="bus.id")
    bu: Optional["BU"] = Relationship(back_populates="users")

    roles: List[Role] = Relationship(
        back_populates="users",
        link_model=UserRoleLink
    )
    
    