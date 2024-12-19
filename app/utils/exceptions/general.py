from fastapi import HTTPException, status


something_went_wrong = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Something went wrong',
    headers={"WWW-Authenticate": "Bearer"},
)