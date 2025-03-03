from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import TeoaCommentModel, TeoaComment

class TeoaCommentRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(TeoaCommentModel, TeoaComment)
        

TeoaCommentRepositoryDep = Annotated[TeoaCommentRepository, Depends(get_repository(TeoaCommentRepository))]