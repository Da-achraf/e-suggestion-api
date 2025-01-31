from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.db.models import IdeaModel


class RatingMatrixBase(SQLModel):
    comments: Optional[str] = None
    quality: int = 0
    cost_reduction: int = 0
    time_savings: int = 0
    ehs: int = 0
    initiative: int = 0
    creativity: int = 0
    transversalization: int = 0
    effectiveness: int = 0
    total_score: float = 0

class RatingMatrixMixin(SQLModel):
    idea_id: Optional[int] = Field(default=None, foreign_key="ideas.id", ondelete='CASCADE')


class RatingMatrixCreate(RatingMatrixBase, RatingMatrixMixin):
    pass

class RatingMatrixModel(RatingMatrixBase, RatingMatrixMixin, table=True):
    __tablename__ = "rating_matrices"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    idea: Optional['IdeaModel'] = Relationship(back_populates='rating_matrix')

    
class RatingMatrix(RatingMatrixBase):
    id: int
    
    class Config:
        from_attributes = True