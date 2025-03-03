from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .assignment_comment import AssignmentComment
from .user import User
from .associations import UserAssignmentLink

if TYPE_CHECKING:
    from .idea import IdeaModel
    from .assignment_comment import AssignmentCommentModel
    from .user import UserModel


class AssignmentBase(SQLModel):
    due_date: Optional[datetime] = Field(default=None)

class AssignmentMixin(SQLModel):
    idea_id: Optional[int] = Field(default=None, foreign_key="ideas.id", ondelete='CASCADE')


class AssignmentCreate(AssignmentBase, AssignmentMixin):
    pass

class AssignmentModel(AssignmentBase, AssignmentMixin, table=True):
    __tablename__ = "assignments"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    comments: list['AssignmentCommentModel'] = Relationship(back_populates='assignment', sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    assignees: list['UserModel'] = Relationship(
        back_populates="assignments", 
        link_model=UserAssignmentLink
    )
    
    idea: Optional['IdeaModel'] = Relationship(back_populates='assignment')
    
class Assignment(AssignmentBase):
    id: int
    comments: list[AssignmentComment]
    assignees: list[User] = []
    
    class Config:
        from_attributes = True