from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .user import User

from sqlalchemy.orm import Mapped

if TYPE_CHECKING:
    from .idea import IdeaModel
    from .user import UserModel


class AttachmentBase(SQLModel):
    name: str = Field(unique=True, max_length=255)
    size: float | None = Field(ge=0, default=None)
    
    
class AttachmentMixin(SQLModel):
    idea_id: Optional[int] = Field(default=None, foreign_key='ideas.id', ondelete='CASCADE')
    uploaded_by: Optional[int] = Field(default=None, foreign_key='users.id', ondelete='CASCADE')


class AttachmentCreate(AttachmentBase, AttachmentMixin):
    file_path: str = Field()


class AttachmentModel(AttachmentBase, AttachmentMixin, table=True):
    __tablename__ = "attachments"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    file_path: str = Field()
    
    # idea: Optional['IdeaModel'] = Relationship(back_populates='attachments')
    idea: Mapped["IdeaModel"] = Relationship(back_populates="attachments")

    uploader: Optional['UserModel'] = Relationship(back_populates='uploads')

    
class Attachment(AttachmentBase):
    id: int = Field()
    file_path: str = Field()
    uploader: User
    
    class Config:
        from_attributes = True