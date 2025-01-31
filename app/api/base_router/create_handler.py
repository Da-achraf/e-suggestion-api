from typing import TypeVar, Type

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.utils.exceptions import something_went_wrong
from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import SessionDep
from app.schemas import Response
from app.api.base_router.base_handler import BaseHandler

from app.api.base_router.shared import ModelType, RequestType, ResponseType


class CreateHandler(BaseHandler[ModelType, ResponseType]):
    def __init__(
        self,
        repository: CRUDBaseRepository[ModelType, ResponseType],
        response_type: Type[ResponseType],
        request_type: Type[RequestType]
    ):
        super().__init__(repository, response_type)
        self.request_type = request_type

    def create_register_item_handler(self):
        async def register_item(
            item_to_save: self.request_type,
            db: SessionDep
        ):
            if not item_to_save:
                raise something_went_wrong
            try:
                db.begin()
                saved_item = self.repository.insert_line(data=item_to_save, db=db)
            except IntegrityError:
                db.rollback()
                self.handle_integrity_error()
            except SQLAlchemyError:
                db.rollback()
                self.handle_transaction_error()
            else:
                db.commit()
                return Response[self.response_type](data=saved_item)

        return register_item