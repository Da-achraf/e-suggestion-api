from typing import Optional, Generic, TypeVar, Union, List
from pydantic import BaseModel


DataT = TypeVar("DataT")


class Response(BaseModel, Generic[DataT]):
    message: Optional[str] = None
    data: Optional[Union[dict, DataT, List[DataT]]] = None
    
    class Config:
        arbitrary_types_allowed = True
        
class ResponseWithPagination(BaseModel, Generic[DataT]):
    message: Optional[str] = None
    content: Union[List[DataT], DataT, None] = None
    page: int = 0
    total: int = 0

    class Config:
        arbitrary_types_allowed = True