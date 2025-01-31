# from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Enum, Column
from datetime import datetime
import enum
from typing import Optional
from .user import UserModel, User
from .attachment import Attachment
from .comment import Comment
from .rating_matrix import RatingMatrix
from .assignment import Assignment

if TYPE_CHECKING:
    from .user import UserModel
    from .attachment import AttachmentModel
    from .comment import CommentModel
    from .rating_matrix import RatingMatrixModel
    from .assignment import AssignmentModel

class IdeaStatus(str, enum.Enum):
    CREATED = "created"
    REJECTED = "rejected"
    APPROVED = "approved"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in progress"
    IMPLEMENTED = "implemented"
    CLOSED = "closed"

    @classmethod
    def as_enum_type(cls):
        # This helper creates a SQLAlchemy Enum type with the values instead of names
        return Enum(
            *[member.value for member in cls],
            name='ideastatus',
            values_callable=lambda obj: [e.value for e in obj]
        )


class IdeaBase(SQLModel):
    title: str = Field()
    actual_situation: str = Field()
    description: str = Field()
    status: IdeaStatus = Field(
        sa_column=Column(IdeaStatus.as_enum_type(), default=IdeaStatus.CREATED),
        default=IdeaStatus.CREATED
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)
    
    
class IdeaMixin(SQLModel):
    submitter_id: Optional[int] = Field(default=None, foreign_key="users.id")
        
    
class IdeaModel(IdeaBase, IdeaMixin, table=True):
    __tablename__ = 'ideas'
    id: Optional[int] = Field(default=None, primary_key=True)
    
    submitter: Optional["UserModel"] = Relationship()
    
    attachments: list['AttachmentModel'] = Relationship(back_populates='idea', cascade_delete=True)
    
    comments: list["CommentModel"] = Relationship(back_populates='idea', cascade_delete=True)
    
    rating_matrix: Optional["RatingMatrixModel"] = Relationship(back_populates='idea', cascade_delete=True)
    
    assignment: Optional["AssignmentModel"] = Relationship(back_populates='idea', cascade_delete=True)
    
    
class IdeaCreate(IdeaBase, IdeaMixin):
    pass


class Idea(IdeaBase):
    id: int
    submitter: User
    attachments: list[Attachment]
    comments: list[Comment]
    rating_matrix: Optional[RatingMatrix]=None
    assignment: Optional[Assignment]=None
    
    class Config:
        from_attributes = True
        
# IdeaModel.model_rebuild()