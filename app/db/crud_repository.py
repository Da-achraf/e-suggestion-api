from typing import Dict, Generic, TypeVar, List, Optional, Any, Type
from sqlmodel import SQLModel, Session, select, func, and_
from datetime import datetime
from sqlmodel import Session
from sqlalchemy.orm import RelationshipProperty
from app.db.dependencies import SessionDep

ModelType = TypeVar("ModelType", bound=SQLModel)
ResponseType = TypeVar("ResponseType", bound=SQLModel)

# ----------------------------------------------
def is_relationship(attribute):
    """
    Check if an InstrumentedAttribute is a relationship.
    """
    return isinstance(attribute.property, RelationshipProperty)

def get_related_model_class(model, relationship):
    """
    Get the related model class for a relationship.
    """
    if isinstance(relationship.property, RelationshipProperty):
        related_model_class = relationship.property.entity.class_
        return related_model_class
    else:
        raise ValueError(f"'{relationship}' is not a relationship.")
# ----------------------------------------------



class CRUDBaseRepository(Generic[ModelType, ResponseType]):
    """
    Generic class for CRUD repository
    """
    def __init__(self, model: ModelType, response_type: Type[ResponseType]) -> None:
        self.model = model
        self.response_type = response_type

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
    
    def count_all(self, db: Session) -> int:
        """
        Count all records in the table using an optimized SQL COUNT query.
        """
        statement = select(func.count()).select_from(self.model)
        result = db.exec(statement).first()
        return result
    
    def count_with_filters(self, db: Session, filters: Dict[str, Dict[str, Any]]) -> int:
        """
        Count records in the table that match the given filters.
        """
        statement = select(func.count()).select_from(self.model)
        statement = self._apply_filters(db, statement, filters)
        result = db.exec(statement).first()
        return result
    
    def find_paginated(self, db: Session, offset: int, limit: int) -> List[ModelType]:
        """
        Fetch paginated records from the table.
        """
        statement = (
            select(self.model)
            .order_by(self.model.id)  # Order by a unique column (e.g., primary key)
            .offset(offset)
            .limit(limit)
        )
        return db.exec(statement).all()
    
    def find_paginated_with_filters(
        self, db: Session, offset: int, limit: int, filters: Dict[str, Dict[str, Any]]
    ) -> List[ModelType]:
        """
        Fetch paginated records from the table that match the given filters.
        """
        statement = select(self.model).order_by(self.model.id)
        statement = self._apply_filters(db, statement, filters)
        statement = statement.offset(offset).limit(limit)
        
        return db.exec(statement).all()    
    
    
    def _apply_filters(self, db, statement, filters: Dict[str, Dict[str, Any]]):
        """
        Apply filters to the SQL statement.
        Supports both direct field filters and relationship field filters.
        """
        filter_conditions = []
        for field, filter_info in filters.items():
            operator = filter_info["operator"]
            value = filter_info["value"]
            
            if "__" in field:
                # Relationship field filter: relationship__field
                relationship_name, related_field = field.split("__", 1)
                
                # Get the relationship attribute
                try:
                    relationship = getattr(self.model, relationship_name)
                except AttributeError:
                    continue
                
                if is_relationship(relationship):
                    # Get the related model class
                    related_model_class = relationship.property.entity.class_
                    
                    # Join the related table
                    statement = statement.join(related_model_class)
                    
                    # Get the related field column
                    try:
                        related_field_column = getattr(related_model_class, related_field)
                    except AttributeError:
                        continue
                
                    # Apply the filter condition on the related field
                    if operator == "eq":
                        filter_conditions.append(related_field_column == value)
                    elif operator == "in":
                        filter_conditions.append(related_field_column.in_(value.split(",")))
                    elif operator == "contains":
                        filter_conditions.append(related_field_column.contains(value))
                    # Add more operators as needed
                else:
                    raise ValueError(f"'{relationship_name}' is not a relationship.")
            else:
                # Direct field filter
                if not hasattr(self.model, field):
                    continue
                
                field_column = getattr(self.model, field)
                if isinstance(field_column.type, datetime):
                    value = datetime.fromisoformat(value)  # Convert string to datetime
                
                if operator == "eq":
                    filter_conditions.append(field_column == value)
                elif operator == "gt":
                    filter_conditions.append(field_column > value)
                elif operator == "lt":
                    filter_conditions.append(field_column < value)
                elif operator == "gte":
                    filter_conditions.append(field_column >= value)
                elif operator == "lte":
                    filter_conditions.append(field_column <= value)
                elif operator == "contains":
                    filter_conditions.append(field_column.contains(value))
                elif operator == "in":
                    filter_conditions.append(field_column.in_(value.split(",")))
                # Add more operators as needed
        
        if filter_conditions:
            statement = statement.where(and_(*filter_conditions))
        return statement
    
    
    # def _apply_filters(self, statement, filters: Dict[str, Dict[str, Any]]):
    #     """
    #     Apply filters to the SQL statement, including filters on related models.
    #     This is a generic implementation that handles all types of relationships.
    #     """
    #     filter_conditions = []
    #     for field, filter_info in filters.items():
    #         operator = filter_info["operator"]
    #         value = filter_info["value"]
            
    #         if hasattr(self.model, field):
    #             field_column = getattr(self.model, field)
                
    #             # Handle relationships
    #             if isinstance(field_column, RelationshipProperty):
    #                 if field_column.secondary is not None:
    #                     # Handle many-to-many relationships
    #                     association_table = field_column.secondary
    #                     related_model = field_column.entity.class_
    #                     related_field = filter_info.get("related_field", "id")
                        
    #                     # Determine the foreign key column in the association table
    #                     fk_column = None
    #                     for column in association_table.columns:
    #                         if column.foreign_keys:
    #                             for fk in column.foreign_keys:
    #                                 if fk.column.table == related_model.__table__:
    #                                     fk_column = column
    #                                     break
    #                         if fk_column:
    #                             break
                        
    #                     if fk_column is None:
    #                         raise ValueError(f"Could not determine foreign key column for relationship: {field}")
                        
    #                     # Join the association table
    #                     statement = statement.join(association_table)
                        
    #                     # Apply the filter condition on the foreign key column
    #                     if operator == "eq":
    #                         filter_conditions.append(fk_column == value)
    #                     elif operator == "in":
    #                         filter_conditions.append(fk_column.in_(value.split(",")))
    #                 else:
    #                     # Handle one-to-many or many-to-one relationships
    #                     related_model = field_column.entity.class_
    #                     related_field = filter_info.get("related_field", "id")
                        
    #                     # Join the related table
    #                     statement = statement.join(related_model)
                        
    #                     # Apply the filter condition on the joined table
    #                     if operator == "eq":
    #                         filter_conditions.append(getattr(related_model, related_field) == value)
    #                     elif operator == "in":
    #                         filter_conditions.append(getattr(related_model, related_field).in_(value.split(",")))
    #             else:
    #                 # Handle regular columns
    #                 if hasattr(field_column, "type") and isinstance(field_column.type, datetime):
    #                     value = datetime.fromisoformat(value)  # Convert string to datetime
                    
    #                 if operator == "eq":
    #                     filter_conditions.append(field_column == value)
    #                 elif operator == "gt":
    #                     filter_conditions.append(field_column > value)
    #                 elif operator == "lt":
    #                     filter_conditions.append(field_column < value)
    #                 elif operator == "gte":
    #                     filter_conditions.append(field_column >= value)
    #                 elif operator == "lte":
    #                     filter_conditions.append(field_column <= value)
    #                 elif operator == "contains":
    #                     filter_conditions.append(field_column.contains(value))
    #                 elif operator == "in":
    #                     filter_conditions.append(field_column.in_(value.split(",")))
    #                 # Add more operators as needed
        
    #     if filter_conditions:
    #         statement = statement.where(and_(*filter_conditions))
    #     return statement


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
    
    def find_parsed_by_id(self, db: Session, model_id: int):
        """
        Find a single record by its ID.
        """
        statement = select(self.model).where(self.model.id == model_id)
        result = db.exec(statement).first()
        if not result: return
        return self.response_type.model_validate(result)

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
            if hasattr(model, field) and field != 'id':
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