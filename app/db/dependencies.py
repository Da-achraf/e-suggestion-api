from fastapi import Depends
from typing import Annotated, Type, TYPE_CHECKING
from sqlmodel import Session
from app.db.base import get_session


SessionDep = Annotated[Session, Depends(get_session)]

if TYPE_CHECKING:
    from app.db.crud_repository import CRUDBaseRepository


def get_repository(repo_type: Type['CRUDBaseRepository']) -> 'CRUDBaseRepository':
    """
    Generic dependency to provide any repository.
    """
    def _get_repo() -> 'CRUDBaseRepository':
        return repo_type()
    return _get_repo