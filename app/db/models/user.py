from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .associations import UserRoleLink
from .bu import BUModel, BU
from .role import Role
from .plant import PlantModel, Plant

if TYPE_CHECKING:
    from .role import RoleModel
    from .attachment import AttachmentModel
    from .comment import CommentModel
    from .assignment_comment import AssignmentCommentModel


class UserBase(SQLModel):
    te_id: str = Field(unique=True, max_length=255)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: str = Field(unique=True, max_length=255)
    account_status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    deactivated_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)
    

class UserLocationMixin(SQLModel):
    bu_id: Optional[int] = Field(default=None, foreign_key="bus.id", ondelete='SET NULL')
    plant_id: Optional[int] = Field(default=None, foreign_key="plants.id", ondelete='SET NULL')


class UserModel(UserBase, UserLocationMixin, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    
    bu: Optional['BUModel'] = Relationship(back_populates='user')
    
    plant: Optional['PlantModel'] = Relationship(back_populates='user')
    
    uploads: List['AttachmentModel'] = Relationship(back_populates='uploader')
    
    comments: List['CommentModel'] = Relationship(back_populates='commenter')
    assignments_comments: List['AssignmentCommentModel'] = Relationship(back_populates='commenter')

    roles: List["RoleModel"] = Relationship(
        back_populates="users",
        link_model=UserRoleLink
    )
    
    
class UserCreate(UserBase, UserLocationMixin):
    password: str = Field()
    role_id: int = Field(default=0)


class UserInDb(UserBase, UserLocationMixin):
    hashed_password: str = Field()
    role_id: int = Field(default=0)


class User(UserBase):
    id: int
    roles: List[Role] = []
    bu: BU
    plant: Plant
    class Config:
        from_attributes = True


class UserWithToken(User):
    token: str = Field()