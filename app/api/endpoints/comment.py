from app.db.models import CommentModel, Comment, CommentCreate
from app.api.base_router import BaseRouter
from app.db.repositories import CommentRepository


class CommentRouter(BaseRouter[CommentModel, Comment]):
    def __init__(self):
        super().__init__(
            repository=CommentRepository(),
            request_type=CommentCreate,
            response_type=Comment
        )

router = CommentRouter().router