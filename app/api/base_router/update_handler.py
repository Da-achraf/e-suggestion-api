
from typing import Dict
from sqlalchemy.exc import SQLAlchemyError
from app.db.dependencies import SessionDep
from app.schemas import Response
from .base_handler import BaseHandler
from app.api.base_router.shared import ModelType, ResponseType


class UpdateHandler(BaseHandler[ModelType, ResponseType]):
    async def update_item_by_id(
        self,
        resource_id: int,
        resource_to_update: Dict,
        db: SessionDep
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
        except SQLAlchemyError:
            db.rollback()
            self.handle_transaction_error()
        else:
            db.commit()
            return Response[self.response_type](data=updated_resource)