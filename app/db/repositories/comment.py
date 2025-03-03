from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import CommentModel, Comment

class CommentRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(CommentModel, Comment)
        

CommentRepositoryDep = Annotated[CommentRepository, Depends(get_repository(CommentRepository))]