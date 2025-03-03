from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .assignment_comment import AssignmentComment

if TYPE_CHECKING:
    from .idea import IdeaModel
    from .teoa_comment import TeoaCommentModel


class TeoaReviewBase(SQLModel):
    ...

class TeoaReviewMixin(SQLModel):
    idea_id: Optional[int] = Field(default=None, foreign_key="ideas.id", ondelete='CASCADE')


class TeoaReviewCreate(TeoaReviewBase, TeoaReviewMixin):
    pass

class TeoaReviewModel(TeoaReviewBase, TeoaReviewMixin, table=True):
    __tablename__ = "teoa_reviews"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    comments: list['TeoaCommentModel'] = Relationship(back_populates='teoa_review', sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    idea: Optional['IdeaModel'] = Relationship(back_populates='teoa_review')
    
class TeoaReview(TeoaReviewBase):
    id: int
    comments: list[AssignmentComment]
    
    class Config:
        from_attributes = True