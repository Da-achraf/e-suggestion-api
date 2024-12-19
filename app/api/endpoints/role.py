from db.models import Role as RoleModel
from schemas import Role
from schemas.role import RoleCreate
from api.base_router import BaseRouter
from db.repositories import RoleRepository


class RoleRouter(BaseRouter[RoleModel, Role]):
    def __init__(self):
        super().__init__(
            repository=RoleRepository(),
            request_type=RoleCreate,
            response_type=Role
        )
        
        
router = RoleRouter().router