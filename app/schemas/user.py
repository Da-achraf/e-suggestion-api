from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from schemas.role import Role

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    account_status: Optional[bool]=False
    
class UserInDb(UserBase):
    hashed_password: str
    
class User(UserBase):
    id: int
    bu_id: Optional[int]=None
    roles: List[Role]
    created_at: datetime
    
    class Config:
        from_attributes = True