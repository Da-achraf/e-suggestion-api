from fastapi import HTTPException, status

transaction_failed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Database transaction Failed',
    headers={"WWW-Authenticate": "Bearer"},
)