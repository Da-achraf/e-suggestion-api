from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository, get_repository
from app.db.models import AssignmentModel, Assignment

class AssignmentRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(AssignmentModel, Assignment)
        

AssignmentRepositoryDep = Annotated[AssignmentRepository, Depends(get_repository(AssignmentRepository))]