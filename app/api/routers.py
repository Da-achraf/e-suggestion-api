from fastapi import APIRouter
from .endpoints import auth, user, bu, role, plant, idea, image, attachment, comment, rating_matrix, assignment

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(role.router, prefix="/roles", tags=["Roles"])
api_router.include_router(bu.router, prefix="/bus", tags=["Business Units"])
api_router.include_router(plant.router, prefix="/plants", tags=["Plants"])
api_router.include_router(idea.router, prefix="/ideas", tags=["Ideas"])
api_router.include_router(image.router, prefix="/images", tags=["Images"])
api_router.include_router(attachment.router, prefix="/attachments", tags=["Attachments"])
api_router.include_router(comment.router, prefix="/comments", tags=["Comments"])
api_router.include_router(rating_matrix.router, prefix="/rating-matrices", tags=["Rating Matrices"])
api_router.include_router(assignment.router, prefix="/assignments", tags=["Ideas Assignments"])