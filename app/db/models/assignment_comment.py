from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .user import User


if TYPE_CHECKING:
    from .user import UserModel
    from .assignment import AssignmentModel


class AssignmentCommentBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    body: str = Field()
    
    
class AssignmentCommentMixin(SQLModel):
    commenter_id: Optional[int] = Field(default=None, foreign_key='users.id', ondelete='CASCADE')
    assignment_id: Optional[int] = Field(default=None, foreign_key='assignments.id')


class AssignmentCommentCreate(AssignmentCommentBase, AssignmentCommentMixin):
    ...


class AssignmentCommentModel(AssignmentCommentBase, AssignmentCommentMixin, table=True):
    __tablename__ = "assignment_comments"
    id: int = Field(primary_key=True)
    
    commenter: Optional['UserModel'] = Relationship(back_populates='assignments_comments')
    assignment: Optional['AssignmentModel'] = Relationship(back_populates='comments')

    
class AssignmentComment(AssignmentCommentBase):
    id: int = Field(primary_key=True)
    commenter: User
    
    class Config:
        from_attributes = True