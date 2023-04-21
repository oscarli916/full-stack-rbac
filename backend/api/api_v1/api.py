from fastapi import APIRouter

from api.api_v1.endpoints import auth, rbac

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(rbac.router, prefix="/rbac", tags=["rbac"])
