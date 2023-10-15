from fastapi.routing import APIRouter

from .order import router as order_router

router = APIRouter(prefix="/v1")
router.include_router(order_router)
