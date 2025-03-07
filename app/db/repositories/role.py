from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import RoleModel, Role

class RoleRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(RoleModel, Role)
        

RoleRepositoryDep = Annotated[RoleRepository, Depends(get_repository(RoleRepository))]