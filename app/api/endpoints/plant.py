from app.db.models import PlantModel, Plant, PlantCreate
from app.api.base_router import BaseRouter
from app.db.repositories import PlantRepository


class PlantRouter(BaseRouter[PlantModel, Plant]):
    def __init__(self):
        super().__init__(
            repository=PlantRepository(),
            request_type=PlantCreate,
            response_type=Plant
        )

router = PlantRouter().router