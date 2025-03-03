from typing import Dict

from app.db.models import AssignmentCommentModel, AssignmentComment, AssignmentCommentCreate
from app.api.base_router import BaseRouter
from app.db.repositories import AssignmentCommentRepository


class AssignmentCommentRouter(BaseRouter[AssignmentCommentModel, AssignmentComment]):
    def __init__(self):
        super().__init__(
            repository=AssignmentCommentRepository(),
            request_type=AssignmentCommentCreate,
            response_type=AssignmentComment
        )


router = AssignmentCommentRouter().router