from typing import Type, Generic, Dict, List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.db.dependencies import SessionDep
from app.db.crud_repository import CRUDBaseRepository
from app.schemas import Response, ResponseWithPagination
from app.api.base_router.shared import ModelType, RequestType, ResponseType
from app.schemas import PatchDeleteReq
from app.utils.exceptions import CustomHTTPException
from app.utils.exceptions.db import transaction_failed
from app.utils.database import parse_filters


async def validate_request_type(request_type, data: Dict) -> RequestType:
    """
    Validate the input data against the request_type Pydantic model.
    """
    if not request_type:
        raise ValidationError('Request type not provided')
    try:
        return request_type(**data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

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
            endpoint=self.all_items,
            methods=["GET"],
            response_model=Response[self.response_type],
            name=f'All {self.model_name}s'
        )
        
        self.router.add_api_route(
            path="",
            endpoint=self.all_items_with_pagination,
            methods=["GET"],
            response_model=ResponseWithPagination[self.response_type],
            name=f'All paginated {self.model_name}s'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.read_item_by_id,
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
    
    
    async def all_items(
        self,
        db: SessionDep
    ):
        items = self.repository.find_all(db=db)
        
        if not items:
            raise CustomHTTPException.no_items_found(self.model_name)
            
        return Response[List[self.response_type]](
            data=items
        )

        
    async def all_items_with_pagination(
        self,
        db: SessionDep,
        request: Request,
        page: Annotated[int, Query(ge=1, description="Page number starting from 1")]=1,
        items_per_page: Annotated[int, Query(ge=1, description="Number of items per page")]=25,
    ):
        offset = (page - 1) * items_per_page
        
        # Extract all query parameters except `page` and `items_per_page`
        query_params = dict(request.query_params)
        query_params.pop("page", None)
        query_params.pop("items_per_page", None)
        
        # Apply filters if any query parameters are provided
        filters = parse_filters(query_params)
        if filters:
            total_items = self.repository.count_with_filters(db=db, filters=filters)
            items = self.repository.find_paginated_with_filters(db, offset=offset, limit=items_per_page, filters=filters)
        else:
            total_items = self.repository.count_all(db=db)
            items = self.repository.find_paginated(db, offset=offset, limit=items_per_page)
            
        if not items:
            raise CustomHTTPException.no_items_found(self.model_name)
            
        return ResponseWithPagination[self.response_type](
            content=items if items else None,
            page=page,
            total=total_items 
        )


    async def read_item_by_id(self, resource_id: int, db: SessionDep):
        item = self.repository.find_by_id(db=db, model_id=resource_id)
        if not item:
            raise CustomHTTPException.item_not_found(self.model_name)
            
        return Response[self.response_type](data=item)
    
    
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
            raise CustomHTTPException.required_field_not_found(self.model_name.lower())

        try:
            
            updated_resource = self.repository.find_by_id_and_update(
                db=db,
                model_id=resource_id,
                data=resource_to_update,
            )
            if not updated_resource:
                raise CustomHTTPException.item_not_found(self.model_name)
                
        except SQLAlchemyError as e:
            db.rollback()
            raise transaction_failed
        else:
            db.commit()
            return Response[self.response_type](data=updated_resource)
    
    
    async def delete_item_by_id(self, resource_id: int, db: SessionDep, internal_kwargs: dict = Depends(lambda: {})):
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            raise CustomHTTPException.item_not_found(self.model_name)
            
        return Response(
            message='Deleted successfully',
        )


    async def delete_items_by_ids(self, patch_delete_Req: PatchDeleteReq, db: SessionDep):
        if patch_delete_Req is None:
            raise CustomHTTPException.item_not_found(self.model_name)

        deleted_items = self.repository.delete_by_ids(db=db, ids=patch_delete_Req.ids)
        if not deleted_items:
            raise CustomHTTPException.item_not_found(self.model_name)

        return Response(message='Deleted successfully')