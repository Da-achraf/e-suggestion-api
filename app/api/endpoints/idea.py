import os
from typing import Annotated
from fastapi import UploadFile, File, Depends, HTTPException, status, Form
import logging

from app.db.models import IdeaModel, Idea, IdeaCreate, AttachmentCreate
from app.schemas import Response
from app.api.base_router import BaseRouter
from app.db.repositories import IdeaRepository, IdeaRepositoryDep, AttachmentRepositoryDep
from app.db.dependencies import SessionDep
from app.utils.exceptions import CustomHTTPException
from app.utils.upload_strategies import LocalDiskUploadStrategy, UploadStrategy
from ...config import IDEA_ATTACHMENTS_DIR


# Configure the upload strategy
def get_upload_strategy():
    return LocalDiskUploadStrategy(upload_dir=IDEA_ATTACHMENTS_DIR)

UploadStrategyDep = Annotated[UploadStrategy, Depends(get_upload_strategy)]

class IdeaRouter(BaseRouter[IdeaModel, Idea]):
    def __init__(self):
        super().__init__(
            repository=IdeaRepository(),
            request_type=IdeaCreate,
            response_type=Idea
        )
        
        @self.router.post('/{idea_id}/attachments', response_model=Response[Idea])
        async def upload_attachement(
            idea_id: int,
            db: SessionDep,
            ideaRepository: IdeaRepositoryDep,
            attachmentRepository: AttachmentRepositoryDep,
            uploadStrategy: UploadStrategyDep,
            uploaded_by: int = Form(...),
            file: UploadFile = File(...)
        ):
            idea = ideaRepository.find_by_id(model_id=idea_id, db=db)
            if not idea or not idea_id:
                raise CustomHTTPException.item_not_found('idea')
            
            if not file:
                raise CustomHTTPException.required_field_not_found('file')
            
            try:
                file_path = await uploadStrategy.upload(file=file, file_name=f'{idea_id}-{file.filename}')
                
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Attachment not uploaded successfully'
                )
                
            try:
                insert_data = AttachmentCreate(
                    name=f'{idea_id}-{file.filename}',
                    uploaded_by=uploaded_by,
                    idea_id=idea_id,
                    size=file.size,
                    file_path=file_path                    
                )
                
                saved_attachment = attachmentRepository.insert_line(data=insert_data, db=db)
                db.commit()
                db.refresh(saved_attachment)
                db.refresh(idea)
                return Response[Idea](
                    data=idea
                )
            except:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Something went wrong.'
                )
        
    async def delete_item_by_id(
        self,
        resource_id: int,
        db: SessionDep,
        attachmentRepository: AttachmentRepositoryDep,
        upload_strategy: UploadStrategyDep
    ):
        deleted_item = self.repository.delete_by_id(db=db, model_id=resource_id)
        if not deleted_item:
            raise CustomHTTPException.item_not_found(self.model_name)
        
        attachments_paths = [attachment.file_path for attachment in deleted_item.attachments]
        
        # Delete each attachment file from the filesystem
        for file_path in attachments_paths:
            try:
                upload_strategy.delete(file_path=file_path)
            except Exception as e:
                # Log the error and continue deleting other files
                logging.error(f"Failed to delete file {file_path}: {e}")
            
        return Response(
            message='Deleted successfully.',
        )

router = IdeaRouter().router