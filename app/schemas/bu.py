from pydantic import BaseModel


class BUBase(BaseModel):
    name: str

class BUCreate(BUBase):
    pass

class BU(BUBase):
    id: int
    
    class Config:
        from_attributes = True