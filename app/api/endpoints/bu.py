from app.db.models import BUModel, BU, BUCreate
from app.api.base_router import BaseRouter
from app.db.repositories import BURepository


class BURouter(BaseRouter[BUModel, BU]):
    def __init__(self):
        super().__init__(
            repository=BURepository(),
            request_type=BUCreate,
            response_type=BU
        )

router = BURouter().router