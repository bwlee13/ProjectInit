from fastapi import  APIRouter
from app.api.endpoints import registration

router = APIRouter()
router.include_router(registration.router, prefix="/signup", tags=["Registration"])
