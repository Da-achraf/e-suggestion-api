from db.models import BU as BUModel
from schemas import BU, BUCreate
from api.base_router import BaseRouter
from db.repositories import BURepository


class BURouter(BaseRouter[BUModel, BU]):
    def __init__(self):
        super().__init__(
            repository=BURepository(),
            request_type=BUCreate,
            response_type=BU
        )
        
        
router = BURouter().router