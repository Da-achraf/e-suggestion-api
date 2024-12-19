from typing import Annotated
from fastapi import Depends

from core.config import get_settings, Settings
from core.security import get_authenticated_user, get_current_user
from schemas import User


AuthenticatedUserDep = Annotated[User, Depends(get_authenticated_user)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]