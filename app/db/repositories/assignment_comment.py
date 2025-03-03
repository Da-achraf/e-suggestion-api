from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import AssignmentCommentModel, AssignmentComment

class AssignmentCommentRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(AssignmentCommentModel, AssignmentComment)
        

AssignmentCommentRepositoryDep = Annotated[AssignmentCommentRepository, Depends(get_repository(AssignmentCommentRepository))]