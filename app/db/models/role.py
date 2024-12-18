from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from db.models.associations import UserRoleLink

class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=255)
    
    # Define the reverse relationship with User
    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink
    )