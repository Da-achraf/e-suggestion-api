from typing import Annotated
from fastapi import Depends

from db.crud_repository import CRUDBaseRepository, get_repository
from db.models import Role

class RoleRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(Role)
        

RoleRepositoryDep = Annotated[RoleRepository, Depends(get_repository(RoleRepository))]