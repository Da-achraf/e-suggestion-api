from app.db.models import TeoaCommentModel, TeoaComment, TeoaCommentCreate
from app.api.base_router import BaseRouter
from app.db.repositories import TeoaCommentRepository


class TeoaCommentRouter(BaseRouter[TeoaCommentModel, TeoaComment]):
    def __init__(self):
        super().__init__(
            repository=TeoaCommentRepository(),
            request_type=TeoaCommentCreate,
            response_type=TeoaComment
        )

router = TeoaCommentRouter().router