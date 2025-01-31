from app.db.models import RoleModel, Role
from app.db.models.role import RoleCreate
from app.api.base_router import BaseRouter
from app.db.repositories import RoleRepository


class RoleRouter(BaseRouter[RoleModel, Role]):
    def __init__(self):
        super().__init__(
            repository=RoleRepository(),
            request_type=RoleCreate,
            response_type=Role
        )
        
        
router = RoleRouter().router