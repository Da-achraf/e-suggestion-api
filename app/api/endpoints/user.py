from db.models import User as UserModel
from schemas import User, UserBase
from api.base_router import BaseRouter
from db.repositories import UserRepository


class UserRouter(BaseRouter[UserModel, User]):
    def __init__(self):
        super().__init__(
            repository=UserRepository(),
            request_type=UserBase,
            response_type=User
        )


router = UserRouter().router