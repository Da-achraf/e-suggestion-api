from app.db.models import AssignmentModel, Assignment, AssignmentCreate
from app.api.base_router import BaseRouter
from app.db.repositories import AssignmentRepository


class AssignmentRouter(BaseRouter[AssignmentModel, Assignment]):
    def __init__(self):
        super().__init__(
            repository=AssignmentRepository(),
            request_type=AssignmentCreate,
            response_type=Assignment
        )
    

router = AssignmentRouter().router