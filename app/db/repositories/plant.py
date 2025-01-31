from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository, get_repository
from app.db.models import PlantModel, Plant

class PlantRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(PlantModel, Plant)
        

PlantRepositoryDep = Annotated[PlantRepository, Depends(get_repository(PlantRepository))]