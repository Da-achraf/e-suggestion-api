from typing import Optional
from sqlmodel import SQLModel, Field

class BU(SQLModel, table=True):
    __tablename__ = "bus"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=255)
    