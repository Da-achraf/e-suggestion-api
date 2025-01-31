
from typing import TypeVar
from app.db.dependencies import SessionDep
from app.schemas import Response
from .base_handler import BaseHandler
from app.schemas import PatchDeleteReq
from app.api.base_router.shared import ModelType, ResponseType


class DeleteHandler(BaseHandler[ModelType, ResponseType]):
    async def delete_item_by_id(self, resource_id: int, db: SessionDep):
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
            self.handle_item_not_found()

        return Response(message='Deleted successfully')