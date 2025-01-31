from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from .associations import UserRoleLink

if TYPE_CHECKING:
    from .user import UserModel

class RoleBase(SQLModel):
    name: str = Field(unique=True, max_length=255)

class RoleCreate(RoleBase):
    pass
    
class RoleModel(RoleBase, table=True):
    __tablename__ = "roles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["UserModel"] = Relationship(
        back_populates="roles",
        link_model=UserRoleLink
    )

class Role(RoleBase):
    id: int = Field()
    
    class Config:
        from_attributes=True
        

class RoleEnum(str, Enum):
    SYSTEM_ADMIN = 'system-admin'
    TEOA = 'teoa'
    COMMITTEE = 'committee'
    SUBMITTER = 'submitter'
    
    