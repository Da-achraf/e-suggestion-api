from typing import Type, Generic, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import BaseModel, ValidationError

from app.api.base_router.create_handler import CreateHandler
from app.api.base_router.read_handler import ReadHandler
from app.db.dependencies import SessionDep
from app.api.base_router.delete_handler import DeleteHandler
from app.db.crud_repository import CRUDBaseRepository
from app.schemas import Response, ResponseWithPagination
from app.api.base_router.shared import ModelType, RequestType, ResponseType
from app.schemas import PatchDeleteReq
from app.utils.exceptions import CustomHTTPException
from app.utils.exceptions.db import transaction_failed
from app.utils.validation import validate_request_type


class BaseRouter(Generic[ModelType, ResponseType]):
    def __init__(
        self,
        request_type: Type[RequestType],
        response_type: Type[ResponseType],
        repository: CRUDBaseRepository[ModelType, ResponseType]
    ):
        self.repository = repository
        self.model_name = repository.model.__name__

        self.request_type = request_type
        self.response_type = response_type
        self.router = APIRouter()

        # Initialize handlers
        # self.create_handler = CreateHandler(repository, response_type, request_type)
        self.read_handler = ReadHandler(repository, response_type)
        # self.delete_handler = DeleteHandler(repository, response_type)

        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route(
            path="",
            endpoint=self.register_item,
            methods=["POST"],
            response_model=Response[self.response_type],
            name=f'Register a new {self.model_name}'
        )

        self.router.add_api_route(
            path="/all",
            endpoint=self.read_handler.all_items,
            methods=["GET"],
            response_model=Response[self.response_type],
            name=f'All {self.model_name}s'
        )
        
        self.router.add_api_route(
            path="",
            endpoint=self.read_handler.all_items_with_pagination,
            methods=["GET"],
            response_model=ResponseWithPagination[self.response_type],
            name=f'All paginated {self.model_name}s'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.read_handler.read_item_by_id,
            methods=["GET"],
            response_model=Response[self.response_type],
            name=f'Get {self.model_name} by id'
        )

        self.router.add_api_route(
            path="/batch-delete",
            endpoint=self.delete_items_by_ids,
            methods=["DELETE"],
            response_model=Response,
            name=f'Delete {self.model_name}s by ids'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.delete_item_by_id,
            methods=["DELETE"],
            response_model=Response,
            name=f'Delete {self.model_name} by id'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.update_item_by_id,
            methods=["PUT"],
            response_model=Response[self.response_type],
            name=f'Update {self.model_name} by id'
        )
    
    
    
    async def register_item(
        self,
        item_to_save: Dict,
        db: SessionDep,
        internal_kwargs: dict = Depends(lambda: {})
    ):
        # Validate the input against self.request_type
        validated_item = await validate_request_type(
            request_type=self.request_type,
            data=item_to_save
        )

        if not validated_item:
            raise ValueError("Item to save cannot be empty")

        try:
            db.begin()
            saved_item = self.repository.insert_line(data=validated_item, db=db)
        except IntegrityError:
            db.rollback()
            raise CustomHTTPException.unique_constraint_violation(self.model_name)

        except SQLAlchemyError:
            db.rollback()
            raise transaction_failed
        else:
            db.commit()
            return Response[self.response_type](data=saved_item)

    
    async def update_item_by_id(
        self,
        resource_id: int,
        resource_to_update: Dict,
        db: SessionDep,
        internal_kwargs: dict = Depends(lambda: {})
    ):
        if not resource_to_update:
            self.handle_required_field_not_found()

        try:
            updated_resource = self.repository.find_by_id_and_update(
                db=db,
                model_id=resource_id,
                data=resource_to_update
            )
            if not updated_resource:
                self.handle_item_not_found()
        except SQLAlchemyError as e:
            db.rollback()
            raise transaction_failed
        else:
            db.commit()
            return Response[self.response_type](data=updated_resource)
    
    async def delete_item_by_id(self, resource_id: int, db: SessionDep, internal_kwargs: dict = Depends(lambda: {})):
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            self.handle_item_not_found()
        return Response(
            message='Deleted successfully',
        )

    async def delete_items_by_ids(self, patch_delete_Req: PatchDeleteReq, db: SessionDep):
        if patch_delete_Req is None:
            self.handle_item_not_found()

        deleted_items = self.repository.delete_by_ids(db=db, ids=patch_delete_Req.ids)
        if not deleted_items:
            raise CustomHTTPException.item_not_found(self.model_name)

        return Response(message='Deleted successfully')