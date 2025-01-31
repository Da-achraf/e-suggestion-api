from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.db.models import UserModel


class PlantBase(SQLModel):
    name: str = Field(unique=True, max_length=255)

class PlantCreate(PlantBase):
    pass


class PlantModel(PlantBase, table=True):
    __tablename__ = "plants"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user: Optional['UserModel'] = Relationship(back_populates='plant')
    
    
class Plant(PlantBase):
    id: int
    
    class Config:
        from_attriPlanttes = True