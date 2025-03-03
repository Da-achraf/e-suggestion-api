from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .user import User


if TYPE_CHECKING:
    from .user import UserModel
    from .teoa_review import TeoaReviewModel


class TeoaCommentBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    body: str = Field()
    
    
class TeoaCommentMixin(SQLModel):
    commenter_id: Optional[int] = Field(default=None, foreign_key='users.id', ondelete='CASCADE')
    teoa_review_id: Optional[int] = Field(default=None, foreign_key='teoa_reviews.id', ondelete='CASCADE')


class TeoaCommentCreate(TeoaCommentBase, TeoaCommentMixin):
    ...


class TeoaCommentModel(TeoaCommentBase, TeoaCommentMixin, table=True):
    __tablename__ = "teoa_comments"
    id: int = Field(primary_key=True)
    
    commenter: Optional['UserModel'] = Relationship(back_populates='teoa_comments')
    teoa_review: Optional['TeoaReviewModel'] = Relationship(back_populates='comments')

    
class TeoaComment(TeoaCommentBase):
    id: int = Field(primary_key=True)
    commenter: User
    
    class Config:
        from_attributes = True