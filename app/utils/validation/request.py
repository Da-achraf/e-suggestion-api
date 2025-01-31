from typing import Dict
from fastapi import HTTPException
from pydantic import ValidationError

from app.api.base_router.shared import RequestType

async def validate_request_type(request_type, data: Dict) -> RequestType:
    """
    Validate the input data against the request_type Pydantic model.
    """
    if not request_type:
        raise ValidationError('Request type not provided')
    try:
        return request_type(**data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())