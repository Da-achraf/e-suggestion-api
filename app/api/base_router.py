from typing import Generic, TypeVar, Type, Dict

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from utils.exceptions import CustomHTTPException
from utils.exceptions.db import transaction_failed
from db.crud_repository import CRUDBaseRepository
from db.dependencies import SessionDep
from schemas import Response, PatchDeleteReq


ModelType = TypeVar("ModelType")
ResponseType = TypeVar("ResponseType")

class BaseRouter(Generic[ModelType, ResponseType]):
    def __init__(self, responseType: Type[ResponseType], repository: CRUDBaseRepository[ModelType]):
        self.repository = repository
        self.responseType = responseType
        self.router = APIRouter(
            tags=[f"{repository.model.__name__}s"]
        )

        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route(
            path="",
            endpoint=self.all_items,
            methods=["GET"],
            response_model=Response[list[self.responseType]],
            name=f'All {self.responseType.__name__}s'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.read_item_by_id,
            methods=["GET"],
            response_model=Response[self.responseType],
            name=f'Get {self.responseType.__name__} by id'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.delete_item_by_id,
            methods=["DELETE"],
            response_model=Response,
            name=f'Delete {self.responseType.__name__} by id'
        )

        self.router.add_api_route(
            path="/patch-delete",
            endpoint=self.delete_items_by_ids,
            methods=["DELETE"],
            response_model=Response,
            name=f'Delete {self.responseType.__name__}s by ids'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.update_item_by_id,
            methods=["PATCH"],
            response_model=Response[self.responseType],
            name=f'Update {self.responseType.__name__} by id'
        )

    async def all_items(self, db: SessionDep):
        items = self.repository.find_all(db=db)
        if not items:
            raise CustomHTTPException.no_items_found(self.repository.model.__name__)
        
        # data = [self.responseType(**item.__dict__) for item in items]
    
        return Response[list[self.responseType]](
            data=items
        )

    async def read_item_by_id(self, resource_id: int, db: SessionDep):
        item = self.repository.find_by_id(db=db, model_id=resource_id)
        if not item:
            raise CustomHTTPException.item_not_found(self.repository.model.__name__)

        return Response[self.responseType](
            data=item
        )

    async def delete_item_by_id(self, resource_id: int, db: SessionDep):
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            raise CustomHTTPException.item_not_found(self.repository.model.__name__)
       
        return Response[self.responseType](
            message='Deleted successfully',
            data=self.responseType(**deleted_item.__dict__)
        )

    async def delete_items_by_ids(self, patch_delete_Req: PatchDeleteReq, db: SessionDep):
        if patch_delete_Req is None: 
            raise CustomHTTPException.item_not_found(self.repository.model.__name__)

        deleted_items = self.repository.delete_by_ids(db=db, ids=patch_delete_Req.ids)
        if not deleted_items:
            raise CustomHTTPException.item_not_found(self.repository.model.__name__)

        return Response(
            message='Deleted successfully'
        )

    async def update_item_by_id(
            self,
            resource_id: int,
            resource_to_update: Dict,
            db: SessionDep
    ):
        if not resource_to_update:
            raise CustomHTTPException.required_field_not_found(self.repository.model.__name__.lower())

        try:
            updated_resource = self.repository.find_by_id_and_update(
                db=db,
                model_id=resource_id,
                data=resource_to_update
            )
            if not updated_resource:
                raise CustomHTTPException.item_not_found(self.repository.model.__name__.lower())
        except SQLAlchemyError as e:
            db.rollback()
            print(e)
            raise transaction_failed
        else:
            db.commit()
            return Response[self.responseType](
                data=updated_resource
            )