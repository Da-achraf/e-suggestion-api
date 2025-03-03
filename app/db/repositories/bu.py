from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import BUModel, BU

class BURepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(BUModel, BU)
        

BURepositoryDep = Annotated[BURepository, Depends(get_repository(BURepository))]