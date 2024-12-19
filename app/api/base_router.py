from typing import Generic, TypeVar, Type, Dict, Callable

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from utils.exceptions import CustomHTTPException, something_went_wrong
from utils.exceptions.db import transaction_failed
from db.crud_repository import CRUDBaseRepository
from db.dependencies import SessionDep
from schemas import Response, PatchDeleteReq


ModelType = TypeVar("ModelType")
ResponseType = TypeVar("ResponseType")
RequestType = TypeVar("RequestType")


class BaseRouter(Generic[ModelType, ResponseType]):
    """
    Generic class to generate classic CRUD endpoints.
    To customize an endpoint, you have to override its method.
    Methods are:
    - `register_item`: Handles the creation of a new item.
    - `all_items`: Retrieves all items.
    - `read_item_by_id`: Retrieves an item by its ID.
    - `delete_item_by_id`: Deletes an item by its ID.
    - `delete_items_by_ids`: Deletes multiple items by their IDs.
    - `update_item_by_id`: Updates an item by its ID.
    """

    def __init__(
        self,
        request_type: Type[RequestType],
        response_type: Type[ResponseType],
        repository: CRUDBaseRepository[ModelType]
    ):
        """
        Initialize the BaseRouter.

        Args:
            request_type (Type[RequestType]): The request model type (e.g., BUCreate).
            response_type (Type[ResponseType]): The response model type.
            repository (CRUDBaseRepository[ModelType]): The repository for database operations.
        """
        self.repository = repository
        self.model_name = repository.model.__name__

        self.request_type = request_type
        self.response_type = response_type
        self.router = APIRouter()

        self.setup_routes()

    def setup_routes(self):
        """
        Use self.router to setup all the endpoints.
        """
        self.router.add_api_route(
            path="",
            endpoint=self.create_register_item_handler(),
            methods=["POST"],
            response_model=Response[self.response_type],
            name=f'Register a new {self.model_name}'
        )

        self.router.add_api_route(
            path="",
            endpoint=self.all_items,
            methods=["GET"],
            response_model=Response[list[self.response_type]],
            name=f'All {self.model_name}s'
        )

        self.router.add_api_route(
            path="/{resource_id}",
            endpoint=self.read_item_by_id,
            methods=["GET"],
            response_model=Response[self.response_type],
            name=f'Get {self.model_name} by id'
        )
     
        self.router.add_api_route(
            path="/patch-delete",
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
            methods=["PATCH"],
            response_model=Response[self.response_type],
            name=f'Update {self.model_name} by id'
        )

    def create_register_item_handler(self) -> Callable:
        """
        Dynamically create the handler for the register_item endpoint.
        This allows us to use self.request_type as the request body type.

        Returns:
            Callable: The dynamically created handler function.
        """
        async def register_item(
            item_to_save: self.request_type,
            db: SessionDep
        ):
            """
            Register a new item.

            Args:
                item_to_save (self.request_type): The item to be saved, matching the request model.
                db (SessionDep): The database session dependency.

            Raises:
                something_went_wrong: If the item_to_save is invalid.
                CustomHTTPException.unique_constraint_violation: If a unique constraint is violated.
                transaction_failed: If a database transaction fails.

            Returns:
                Response[self.response_type]: The saved item wrapped in a Response object.
            """
            if not item_to_save:
                raise something_went_wrong
            try:
                db.begin()
                saved_item: self.response_type = self.repository.insert_line(data=item_to_save, db=db)

            except IntegrityError as e:
                db.rollback()
                raise CustomHTTPException.unique_constraint_violation(self.model_name)
            except SQLAlchemyError:
                db.rollback()
                raise transaction_failed
            else:
                db.commit()
                return Response[self.response_type](
                    data=saved_item
                )

        return register_item

    async def all_items(self, db: SessionDep):
        """
        Retrieve all items.

        Args:
            db (SessionDep): The database session dependency.

        Raises:
            CustomHTTPException.no_items_found: If no items are found.

        Returns:
            Response[list[self.response_type]]: A list of all items wrapped in a Response object.
        """
        items = self.repository.find_all(db=db)
        if not items:
            raise CustomHTTPException.no_items_found(self.model_name)

        return Response[list[self.response_type]](
            data=items
        )

    async def read_item_by_id(self, resource_id: int, db: SessionDep):
        """
        Retrieve an item by its ID.

        Args:
            resource_id (int): The ID of the item to retrieve.
            db (SessionDep): The database session dependency.

        Raises:
            CustomHTTPException.item_not_found: If the item is not found.

        Returns:
            Response[self.response_type]: The retrieved item wrapped in a Response object.
        """
        item = self.repository.find_by_id(db=db, model_id=resource_id)
        if not item:
            raise CustomHTTPException.item_not_found(self.model_name)

        return Response[self.response_type](
            data=item
        )

    async def delete_item_by_id(self, resource_id: int, db: SessionDep):
        """
        Delete an item by its ID.

        Args:
            resource_id (int): The ID of the item to delete.
            db (SessionDep): The database session dependency.

        Raises:
            CustomHTTPException.item_not_found: If the item is not found.

        Returns:
            Response[self.response_type]: A success message and the deleted item wrapped in a Response object.
        """
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            raise CustomHTTPException.item_not_found(self.model_name)

        return Response[self.response_type](
            message='Deleted successfully',
            data=self.response_type(**deleted_item.__dict__)
        )

    async def delete_items_by_ids(self, patch_delete_Req: PatchDeleteReq, db: SessionDep):
        """
        Delete multiple items by their IDs.

        Args:
            patch_delete_Req (PatchDeleteReq): The request containing the list of IDs to delete.
            db (SessionDep): The database session dependency.

        Raises:
            CustomHTTPException.item_not_found: If no items are found.

        Returns:
            Response: A success message wrapped in a Response object.
        """
        if patch_delete_Req is None:
            raise CustomHTTPException.item_not_found(self.model_name)

        deleted_items = self.repository.delete_by_ids(db=db, ids=patch_delete_Req.ids)
        if not deleted_items:
            raise CustomHTTPException.item_not_found(self.model_name)

        return Response(
            message='Deleted successfully'
        )

    async def update_item_by_id(
        self,
        resource_id: int,
        resource_to_update: Dict,
        db: SessionDep
    ):
        """
        Update an item by its ID.

        Args:
            resource_id (int): The ID of the item to update.
            resource_to_update (Dict): The data to update the item with.
            db (SessionDep): The database session dependency.

        Raises:
            CustomHTTPException.required_field_not_found: If no update data is provided.
            CustomHTTPException.item_not_found: If the item is not found.
            transaction_failed: If a database transaction fails.

        Returns:
            Response[self.response_type]: The updated item wrapped in a Response object.
        """
        if not resource_to_update:
            raise CustomHTTPException.required_field_not_found(self.model_name.lower())

        try:
            updated_resource = self.repository.find_by_id_and_update(
                db=db,
                model_id=resource_id,
                data=resource_to_update
            )
            if not updated_resource:
                raise CustomHTTPException.item_not_found(self.model_name.lower())
        except SQLAlchemyError:
            db.rollback()
            raise transaction_failed
        else:
            db.commit()
            return Response[self.response_type](
                data=updated_resource
            )