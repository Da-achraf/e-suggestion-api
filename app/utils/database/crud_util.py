from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import RelationshipProperty
from sqlmodel import and_, Column, SQLModel


# def parse_filters(query_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
#     """
#     Parse query parameters into a filters dictionary.
#     Supports direct field filters (field__op=value) and nested relationship field filters
#     (relationship__nested_relationship__field__op=value).
#     """
#     filters = {}
#     for key, value in query_params.items():
#         if "__" in key:
#             parts = key.split("__")
#             if len(parts) == 2:
#                 # Direct field filter: field__op=value
#                 field, operator = parts
#                 filters[field] = {"operator": operator, "value": value}
            
#             elif len(parts) == 3:
#                 # Relationship field filter: relationship__field__op=value
#                 relationship, related_field, operator = parts
#                 filters[f"{relationship}__{related_field}"] = {"operator": operator, "value": value}
            
#             elif len(parts) == 4:
#                 # Nested relationship field filter: relationship__nested_relationship__field__op=value
#                 relationship, nested_relationship, related_field, operator = parts
#                 filters[f"{relationship}__{nested_relationship}__{related_field}"] = {
#                     "operator": operator,
#                     "value": value,
#                 }
            
#             else:
#                 raise ValueError(f"Invalid filter key: {key}")
#         else:
#             # Default to equality for direct field filters
#             filters[key] = {"operator": "eq", "value": value}
#     return filters

# def apply_filters(model, statement, filters: Dict[str, Dict[str, Any]]):
#     """
#     Apply filters to the SQL statement.
#     Supports both direct field filters and relationship field filters.
#     """
#     filter_conditions = []
#     for field, filter_info in filters.items():
#         operator = filter_info["operator"]
#         value = filter_info["value"]
        
#         if "__" in field:
#             # Relationship field filter: relationship__field
#             relationship_name, related_field = field.split("__", 1)
            
#             # Get the relationship attribute
#             try:
#                 relationship = getattr(model, relationship_name)
#             except AttributeError:
#                 continue
            
#             if is_relationship(relationship):
#                 # Get the related model class
#                 # related_model_class = relationship.property.entity.class_
#                 related_model_class = get_related_model_class(relationship=relationship)
                
#                 # Join the related table
#                 statement = statement.join(related_model_class)
                
#                 # Get the related field column
#                 try:
#                     related_field_column: Column = getattr(related_model_class, related_field)
#                 except AttributeError:
#                     continue
            
#                 # Apply the filter condition on the related field
#                 if operator == "eq":
#                     filter_conditions.append(related_field_column == value)
#                 elif operator == "in":
#                     filter_conditions.append(related_field_column.in_(value.split(",")))
#                 elif operator == "contains":
#                     filter_conditions.append(related_field_column.contains(value))
#                 elif operator == "startswith":
#                     filter_conditions.append(related_field_column.startswith(value))
#                 elif operator == "endswith":
#                     filter_conditions.append(related_field_column.endswith(value))
#             else:
#                 raise ValueError(f"'{relationship_name}' is not a relationship.")
#         else:
#             # Direct field filter
#             if not hasattr(model, field):
#                 continue
            
#             field_column: Column = getattr(model, field)
#             if isinstance(field_column.type, datetime):
#                 value = datetime.fromisoformat(value)  # Convert string to datetime
            
#             if operator == "eq":
#                 filter_conditions.append(field_column == value)
#             elif operator == "gt":
#                 filter_conditions.append(field_column > value)
#             elif operator == "lt":
#                 filter_conditions.append(field_column < value)
#             elif operator == "gte":
#                 filter_conditions.append(field_column >= value)
#             elif operator == "lte":
#                 filter_conditions.append(field_column <= value)
#             elif operator == "contains":
#                 filter_conditions.append(field_column.contains(value))
#             elif operator == "startswith":
#                 filter_conditions.append(field_column.startswith(value))
#             elif operator == "endswith":
#                 filter_conditions.append(field_column.endswith(value))
#             elif operator == "in":
#                 filter_conditions.append(field_column.in_(value.split(",")))
    
#     if filter_conditions:
#         statement = statement.where(and_(*filter_conditions))
#     return statement


# def is_relationship(attribute):
#     """
#     Check if an InstrumentedAttribute is a relationship.
#     """
#     return isinstance(attribute.property, RelationshipProperty)


# def get_related_model_class(relationship):
#     """
#     Get the related model class for a relationship.
#     """
#     if isinstance(relationship.property, RelationshipProperty):
#         related_model_class = relationship.property.entity.class_
#         return related_model_class
#     else:
#         raise ValueError(f"'{relationship}' is not a relationship.")



# ----------------------------------------------------------------------------------


def parse_filters(query_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Parse query parameters into a filters dictionary, supporting nested relationships and operators.
    """
    valid_operators = {'eq', 'gt', 'lt', 'gte', 'lte', 'contains', 'startswith', 'endswith', 'in'}
    filters = {}
    for key, value in query_params.items():
        parts = key.split('__')
        operator = 'eq'  # default operator
        # Check if the last part is a valid operator
        if len(parts) > 1 and parts[-1] in valid_operators:
            operator = parts.pop()  # Remove the operator part
            field_path = '__'.join(parts)
        else:
            field_path = key  # No operator in key, use entire key as field path
        filters[field_path] = {'operator': operator, 'value': value}
    return filters


def apply_filters(model: SQLModel, statement, filters: Dict[str, Dict[str, Any]]):
    """
    Apply filters to the SQL statement, handling nested relationships by dynamically joining models.
    """
    filter_conditions = []
    for field_path, filter_info in filters.items():
        operator = filter_info["operator"]
        value = filter_info["value"]
        parts = field_path.split('__')
        if len(parts) == 1:
            # Direct field filter
            field_name = parts[0]
            if not hasattr(model, field_name):
                continue
            field_column = getattr(model, field_name)
            # Handle datetime conversion
            if isinstance(field_column.type, datetime):
                value = datetime.fromisoformat(value)
            # Create condition
            try:
                condition = create_condition(field_column, operator, value)
                filter_conditions.append(condition)
            except ValueError:
                continue  # Skip invalid operator
        else:
            # Nested relationship filter
            current_model = model
            valid_relationship = True
            for part in parts[:-1]:
                if not hasattr(current_model, part):
                    valid_relationship = False
                    break
                attr = getattr(current_model, part)
                if not is_relationship(attr):
                    valid_relationship = False
                    break
                # Join the relationship
                statement = statement.join(attr)
                current_model = get_related_model_class(attr)
            if not valid_relationship:
                continue  # Skip invalid path
            # Check if the final model has the field
            field_name = parts[-1]
            if not hasattr(current_model, field_name):
                continue
            field_column = getattr(current_model, field_name)
            # Handle datetime conversion
            if isinstance(field_column.type, datetime):
                value = datetime.fromisoformat(value)
            # Create condition
            try:
                condition = create_condition(field_column, operator, value)
                filter_conditions.append(condition)
            except ValueError:
                continue  # Skip invalid operator
    if filter_conditions:
        statement = statement.where(and_(*filter_conditions))
    return statement


def is_relationship(attribute) -> bool:
    """Check if an attribute is a relationship."""
    return isinstance(attribute.property, RelationshipProperty)


def get_related_model_class(relationship) -> SQLModel:
    """Get the related model class from a relationship property."""
    return relationship.property.entity.class_


def create_condition(field_column: Column, operator: str, value: Any):
    """Create a SQL condition based on the operator and value."""
    if operator == "eq":
        return field_column == value
    elif operator == "gt":
        return field_column > value
    elif operator == "lt":
        return field_column < value
    elif operator == "gte":
        return field_column >= value
    elif operator == "lte":
        return field_column <= value
    elif operator == "contains":
        return field_column.contains(value)
    elif operator == "startswith":
        return field_column.startswith(value)
    elif operator == "endswith":
        return field_column.endswith(value)
    elif operator == "in":
        if isinstance(value, str):
            value = value.split(",")
        return field_column.in_(value)
    else:
        raise ValueError(f"Unsupported operator: {operator}")