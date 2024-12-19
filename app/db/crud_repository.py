from typing import Dict, Generic, TypeVar, List, Optional
from sqlmodel import SQLModel, Session, select
from typing import Type
from fastapi import Depends
from sqlmodel import Session
from db.dependencies import SessionDep

ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBaseRepository(Generic[ModelType]):
    """
    Generic class for CRUD repository
    """
    def __init__(self, model: ModelType) -> None:
        self.model = model

    def insert_line(self, db: Session, data: SQLModel):
        """
        Insert a new record into the database.
        """
        record = self.model(**data.model_dump())  # Convert Pydantic/SQLModel model to dict
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record

    def delete_by_ids(self, db: Session, ids: List[int]):
        """
        Delete multiple records by their IDs.
        """
        items = []
        for id in ids:
            deleted_item = self.delete_by_id(db=db, model_id=id)
            if deleted_item:
                items.append(deleted_item)

        if len(items) != len(ids):
            return None
        return items

    def find_by_ids(self, db: Session, ids: List[int]) -> List[ModelType]:
        """
        Find multiple records by their IDs.
        """
        statement = select(self.model).where(self.model.id.in_(ids))
        results = db.exec(statement).all()
        return results

    def find_by_id(self, db: Session, model_id: int) -> Optional[ModelType]:
        """
        Find a single record by its ID.
        """
        statement = select(self.model).where(self.model.id == model_id)
        result = db.exec(statement).first()
        return result

    def find_all(self, db: Session) -> List[ModelType]:
        """
        Find all records of the model.
        """
        statement = select(self.model)
        results = db.exec(statement).all()
        return results

    def find_by_id_and_update(self, db: Session, model_id: int, data: Dict):
        """
        Find a record by its ID and update it with the provided data.
        """
        model = self.find_by_id(db=db, model_id=model_id)
        if not model:
            return None

        for field, value in data.items():
            # Check if the field exists in the model
            if hasattr(model, field):
                setattr(model, field, value)
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    @staticmethod
    def _delete(db: Session, model: ModelType) -> None:
        """
        Delete a single record from the database.
        """
        db.delete(model)
        db.commit()

    def delete_by_id(self, db: Session, model_id: int):
        """
        Delete a single record by its ID.
        """
        model = self.find_by_id(db, model_id)
        if model:
            self._delete(db=db, model=model)
            return model
        return None
    
    
def get_repository(repo_type: Type[CRUDBaseRepository]) -> CRUDBaseRepository:
    """
    Generic dependency to provide any repository.
    """
    def _get_repo(db: SessionDep) -> CRUDBaseRepository:
        return repo_type()
    return _get_repo