from typing import List
from fastapi import APIRouter, Depends, HTTPException


from schemas.order import ProductOrder, CrateCounts
from persistance.load_data import get_data_provider, DataProvider
from core.crate_optimizer import CrateOptimizer
from exceptions.persistance import ProductNotFound


router = APIRouter(tags=["Orders"], prefix="/orders")


@router.post(
    "/dispatch",
    response_model=CrateCounts
)
def dispatch_order(
    order_products: List[ProductOrder],
    data_provider: DataProvider = Depends(get_data_provider)
):
    try:
        crate_optimzer = CrateOptimizer(order_products, data_provider)
        return crate_optimzer.calculate_optimal_crates()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception:
        raise HTTPException(status_code=500, detail="Unknown error.")

