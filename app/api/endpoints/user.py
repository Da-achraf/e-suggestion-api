from typing import Dict

from app.schemas.response import Response
from app.db.models import UserModel, UserBase, User, UserWithToken
from app.core.security import generate_tokens
from app.core.config import SettingsDep
from app.db.dependencies import SessionDep
from app.utils.exceptions import CustomHTTPException
from app.api.base_router import BaseRouter
from app.db.repositories import UserRepository, UserRepositoryDep, RoleRepositoryDep


class UserRouter(BaseRouter[UserModel, User]):
    def __init__(self):
        super().__init__(
            repository=UserRepository(),
            request_type=UserBase,
            response_type=User
        )
        
        @self.router.get('/{user_id}/with-token', response_model=Response[UserWithToken])
        async def get_user_with_token(user_id: int, db: SessionDep, settings: SettingsDep):
            user = self.repository.find_by_id(model_id=user_id, db=db)
            if not user:
                raise CustomHTTPException.item_not_found('user')

            access_token, _ = generate_tokens(user=User.model_validate(user), settings=settings.JWT)
            user_with_token = UserWithToken(**User.model_validate(user).model_dump(), token=access_token)

            return Response[UserWithToken](
                data=user_with_token
            )
    
    async def update_item_by_id(
        self,
        resource_id: int,
        resource_to_update: Dict,
        db: SessionDep,
        user_repository: UserRepositoryDep,
        role_repository: RoleRepositoryDep
    ):  
        try:
            response = await super().update_item_by_id(
                resource_id=resource_id,
                resource_to_update=resource_to_update,
                db=db
            )
        except:
            raise
        else:
            if 'role_id' in resource_to_update.keys():
                role = role_repository.find_by_id(db=db, model_id=resource_to_update['role_id'])
                
                if not role:
                    return response
                
                user = user_repository.find_by_id(db=db, model_id=resource_id)
                user.roles.clear()
                user.roles.append(role)
                db.commit()
                
                return Response[self.response_type](data=user)
                
            return response
        

router = UserRouter().router