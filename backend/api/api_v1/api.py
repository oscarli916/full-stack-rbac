from fastapi import APIRouter

from api.api_v1.endpoints import auth, permission, user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(permission.router, prefix="/rbac/permission", tags=["rbac"])
api_router.include_router(user.router, prefix="/rbac/user", tags=["rbac"])
