from fastapi import HTTPException, status


credentials_already_taken = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Username or email already taken',
    headers={"WWW-Authenticate": "Bearer"},
)

item_not_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Item not found',
    headers={"WWW-Authenticate": "Bearer"},
)

no_items_found = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='No items were found',
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate token",
    headers={"WWW-Authenticate": "Bearer"},
)

incorrect_credentials = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Incorrect username or password',
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid email address',
    headers={"WWW-Authenticate": "Bearer"},
)

passwords_mismatch = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Passwords do not match',
    headers={"WWW-Authenticate": "Bearer"},
)

account_not_approved = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Your account is not approved',
    headers={"WWW-Authenticate": "Bearer"},
)

transaction_failed = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Transaction Failed',
    headers={"WWW-Authenticate": "Bearer"},
)

something_went_wrong = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Something went wrong',
    headers={"WWW-Authenticate": "Bearer"},
)

