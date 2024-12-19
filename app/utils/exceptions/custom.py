from fastapi import HTTPException, status


class CustomHTTPException:
    @staticmethod
    def item_not_found(item_name: str):
        detail = f"{item_name.capitalize()} not found"
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

    @staticmethod
    def item_already_exists(item_name: str):
        detail = f"{item_name.capitalize()} already exists"
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    @staticmethod
    def no_items_found(item_name: str):
        detail = f"No {item_name}s were found"
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

    @staticmethod
    def required_field_not_found(field: str):
        detail = f"Required field '{field}' not found"
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
        
    @staticmethod
    def unique_constraint_violation(model_name: str):
        detail = f"Unique contraint violated for model '{model_name}'"
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )