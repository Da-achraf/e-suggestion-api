from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.db.models import UserModel


class BUBase(SQLModel):
    name: str = Field(unique=True, max_length=255)

class BUCreate(BUBase):
    pass


class BUModel(BUBase, table=True):
    __tablename__ = "bus"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user: Optional['UserModel'] = Relationship(back_populates='bu')
    
class BU(BUBase):
    id: int
    
    class Config:
        from_attributes = True