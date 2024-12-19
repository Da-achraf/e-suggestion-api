from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError

from db.models import User as UserModel
from schemas import User
from api.base_router import BaseRouter
from db.repositories import UserRepositoryDep
from db.crud_repository import get_repository

from db.repositories.user import UserRepository


class UserRouter(BaseRouter[UserModel, User]):
    def __init__(self, repository: UserRepository, responseType):
        super().__init__(responseType=responseType, repository=repository)


user_repo = UserRepository()

router = UserRouter(
    responseType=User,
    repository=user_repo
).router