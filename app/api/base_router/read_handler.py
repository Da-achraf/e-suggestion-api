
from typing import Type, Annotated, Any, Dict, List
from fastapi import Query, Request
from app.db.dependencies import SessionDep
from app.schemas import Response, ResponseWithPagination
from .base_handler import BaseHandler
from app.db.crud_repository import CRUDBaseRepository
from app.api.base_router.shared import ModelType, ResponseType

def parse_filters(query_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Parse query parameters into a filters dictionary.
    Supports both direct field filters (field__op=value) and relationship field filters (relationship__field__op=value).
    """
    filters = {}
    for key, value in query_params.items():
        if "__" in key:
            parts = key.split("__")
            if len(parts) == 2:
                # Direct field filter: field__op=value
                field, operator = parts
                filters[field] = {"operator": operator, "value": value}
            elif len(parts) == 3:
                # Relationship field filter: relationship__field__op=value
                relationship, related_field, operator = parts
                filters[f"{relationship}__{related_field}"] = {"operator": operator, "value": value}
            else:
                raise ValueError(f"Invalid filter key: {key}")
        else:
            # Default to equality for direct field filters
            filters[key] = {"operator": "eq", "value": value}
    return filters


class ReadHandler(BaseHandler[ModelType, ResponseType]):
    def __init__(
        self,
        repository: CRUDBaseRepository[ModelType, ResponseType],
        response_type: Type[ResponseType]
    ):
        self.repository = repository
        self.response_type = response_type
        self.model_name = repository.model.__name__
    
    async def all_items(
        self,
        db: SessionDep
    ):
        items = self.repository.find_all(db=db)
        
        if not items:
            self.handle_no_items_found()
            
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
            self.handle_no_items_found()
            
        return ResponseWithPagination[self.response_type](
            content=items if items else None,
            page=page,
            total=total_items 
        )

    async def read_item_by_id(self, resource_id: int, db: SessionDep):
        item = self.repository.find_by_id(db=db, model_id=resource_id)
        if not item:
            self.handle_item_not_found()
        return Response[self.response_type](data=item)
    
    
    
  