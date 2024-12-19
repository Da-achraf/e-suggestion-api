from fastapi import APIRouter
from api.endpoints import auth, user, bu, role

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(role.router, prefix="/roles", tags=["Roles"])
api_router.include_router(bu.router, prefix="/bus", tags=["Business Units"])