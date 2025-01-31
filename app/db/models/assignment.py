from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .assignment_comment import AssignmentComment

if TYPE_CHECKING:
    from .idea import IdeaModel
    from .assignment_comment import AssignmentCommentModel


class AssignmentBase(SQLModel):
    due_date: Optional[datetime] = Field(default=None)

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentMixin(SQLModel):
    idea_id: Optional[int] = Field(default=None, foreign_key="ideas.id", ondelete='CASCADE')


class AssignmentModel(AssignmentBase, AssignmentMixin, table=True):
    __tablename__ = "assignments"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    comments: list['AssignmentCommentModel'] = Relationship(back_populates='assignment')
    
    idea: Optional['IdeaModel'] = Relationship(back_populates='assignment')
    
class Assignment(AssignmentBase):
    id: int
    comments: list[AssignmentComment]
    
    class Config:
        from_attributes = True