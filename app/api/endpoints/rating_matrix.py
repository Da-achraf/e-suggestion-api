from app.db.models import RatingMatrixModel, RatingMatrix, RatingMatrixCreate
from app.api.base_router import BaseRouter
from app.db.repositories import RatingMatrixRepository


class RatingMatrixRouter(BaseRouter[RatingMatrixModel, RatingMatrix]):
    def __init__(self):
        super().__init__(
            repository=RatingMatrixRepository(),
            request_type=RatingMatrixCreate,
            response_type=RatingMatrix
        )

router = RatingMatrixRouter().router