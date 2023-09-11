from fastapi import APIRouter

from .users import router as users_router
from .oneways import router as oneways_router

router = APIRouter(prefix="/api/v1", tags=["api"])

router.include_router(users_router)
router.include_router(oneways_router)
