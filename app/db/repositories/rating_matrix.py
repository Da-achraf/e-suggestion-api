from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import RatingMatrixModel, RatingMatrix

class RatingMatrixRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(RatingMatrixModel, RatingMatrix)
        

RatingMatrixRepositoryDep = Annotated[RatingMatrixRepository, Depends(get_repository(RatingMatrixRepository))]