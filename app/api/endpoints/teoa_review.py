from app.db.models import TeoaReviewModel, TeoaReview, TeoaReviewCreate
from app.api.base_router import BaseRouter
from app.db.repositories import TeoaReviewRepository


class TeoaReviewRouter(BaseRouter[TeoaReviewModel, TeoaReview]):
    def __init__(self):
        super().__init__(
            repository=TeoaReviewRepository(),
            request_type=TeoaReviewCreate,
            response_type=TeoaReview
        )

router = TeoaReviewRouter().router