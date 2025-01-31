from typing import Annotated
from fastapi import Depends

from app.core.config import get_settings, Settings
from app.core.security import get_authenticated_user, get_current_user
from app.db.models import User


AuthenticatedUserDep = Annotated[User, Depends(get_authenticated_user)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]