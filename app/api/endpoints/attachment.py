from typing import Annotated
from fastapi import Depends

from app.db.models import AttachmentModel, Attachment, AttachmentCreate
from app.api.base_router import BaseRouter
from app.db.dependencies import SessionDep
from app.db.repositories import AttachmentRepository
from app.utils.upload_strategies import LocalDiskUploadStrategy, UploadStrategy
from app.schemas import Response
from app.utils.exceptions import CustomHTTPException
from app.utils.exceptions.db import transaction_failed


IDEA_ATTACHMENTS_DIR = "../static/ideas-attachments"

# Configure the upload strategy
def get_upload_strategy():
    return LocalDiskUploadStrategy(upload_dir=IDEA_ATTACHMENTS_DIR)

UploadStrategyDep = Annotated[UploadStrategy, Depends(get_upload_strategy)]

class AttachmentRouter(BaseRouter[AttachmentModel, Attachment]):
    def __init__(self):
        super().__init__(
            repository=AttachmentRepository(),
            request_type=AttachmentCreate,
            response_type=Attachment
        )
    
    async def delete_item_by_id(self, resource_id, db: SessionDep, upload_strategy: UploadStrategyDep):
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            raise CustomHTTPException.item_not_found(self.model_name)
        upload_strategy.delete(file_path=deleted_item.file_path)
            
        return Response(
            message='Deleted successfully.',
        )
        

router = AttachmentRouter().router