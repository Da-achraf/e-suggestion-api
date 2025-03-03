from typing import Annotated
from fastapi import Depends

from app.db.crud_repository import CRUDBaseRepository
from app.db.dependencies import get_repository
from app.db.models import AttachmentModel, Attachment

class AttachmentRepository(CRUDBaseRepository):
    def __init__(self) -> None:
        super().__init__(AttachmentModel, Attachment)
        

AttachmentRepositoryDep = Annotated[AttachmentRepository, Depends(get_repository(AttachmentRepository))]