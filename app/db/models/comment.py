from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .user import User


if TYPE_CHECKING:
    from .idea import IdeaModel
    from .user import UserModel
    from .assignment import AssignmentModel


class CommentBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    likes: int = Field(ge=0, default=0)
    body: str = Field()
    
    
class CommentMixin(SQLModel):
    commenter_id: Optional[int] = Field(default=None, foreign_key='users.id', ondelete='CASCADE')
    idea_id: Optional[int] = Field(default=None, foreign_key='ideas.id', ondelete='CASCADE')


class CommentCreate(CommentBase, CommentMixin):
    ...


class CommentModel(CommentBase, CommentMixin, table=True):
    __tablename__ = "comments"
    id: int = Field(primary_key=True)
    
    commenter: Optional['UserModel'] = Relationship(back_populates='comments')
    idea: Optional['IdeaModel'] = Relationship(back_populates='comments')
    # assignment: Optional['AssignmentModel'] = Relationship(back_populates='comments')

    
class Comment(CommentBase):
    id: int = Field(primary_key=True)
    commenter: User
    
    class Config:
        from_attributes = True