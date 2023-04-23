from fastapi import APIRouter

from api.api_v1.endpoints import auth, permission

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(permission.router, prefix="/rbac/permission", tags=["rbac"])
