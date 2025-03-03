from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import TeoaReviewModel, TeoaReview

class TeoaReviewRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(TeoaReviewModel, TeoaReview)
        

TeoaReviewRepositoryDep = Annotated[TeoaReviewRepository, Depends(get_repository(TeoaReviewRepository))]