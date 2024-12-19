from typing import Optional, Generic, TypeVar, Union

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Response(BaseModel, Generic[DataT]):
    message: Optional[str] = None
    data: Optional[Union[dict, DataT]] = None
    
    class Config:
        arbitrary_types_allowed = True