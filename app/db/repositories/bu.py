from typing import Annotated
from fastapi import Depends

from db.crud_repository import CRUDBaseRepository, get_repository
from db.models import BU

class BURepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(BU)
        

BURepositoryDep = Annotated[BURepository, Depends(get_repository(BURepository))]