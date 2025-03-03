from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session, select

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import IdeaModel, Idea

class IdeaRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(IdeaModel, Idea)
        

IdeaRepositoryDep = Annotated[IdeaRepository, Depends(get_repository(IdeaRepository))]