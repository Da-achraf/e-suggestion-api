from typing import Generic, Type

from app.utils.exceptions import CustomHTTPException
from app.utils.exceptions.db import transaction_failed
from app.db.crud_repository import CRUDBaseRepository
from app.api.base_router.shared import ModelType, ResponseType



class BaseHandler(Generic[ModelType, ResponseType]):
    def __init__(
        self,
        repository: CRUDBaseRepository[ModelType, ResponseType],
        response_type: Type[ResponseType]
    ):
        self.repository = repository
        self.response_type = response_type
        self.model_name = repository.model.__name__

    def handle_integrity_error(self):
        """Handle unique constraint violations."""
        raise CustomHTTPException.unique_constraint_violation(self.model_name)

    def handle_transaction_error(self):
        """Handle database transaction errors."""
        raise transaction_failed

    def handle_item_not_found(self):
        """Handle cases where an item is not found."""
        raise CustomHTTPException.item_not_found(self.model_name)

    def handle_no_items_found(self):
        """Handle cases where no items are found."""
        raise CustomHTTPException.no_items_found(self.model_name)

    def handle_required_field_not_found(self):
        """Handle cases where required fields are missing."""
        raise CustomHTTPException.required_field_not_found(self.model_name.lower())