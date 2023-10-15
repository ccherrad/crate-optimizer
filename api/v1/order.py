from typing import List

from fastapi import APIRouter, Depends, HTTPException

from core.crate_optimizer import CrateOptimizer
from exceptions.persistance import ProductNotFound
from persistance.load_data import DataProvider, get_data_provider
from schemas.order import CrateCounts, ProductOrder

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.post("/dispatch", response_model=CrateCounts)
def dispatch_order(
    order_products: List[ProductOrder],
    data_provider: DataProvider = Depends(get_data_provider),
):
    """
    Dispatch an order by calculating optimal crates.

    Parameters:
    - `order_products` (List[ProductOrder]): A list of product orders to be dispatched.
    - `data_provider` (DataProvider): An optional dependency for providing data required for crate optimization.

    Returns:
    - `CrateCounts`: The optimal distribution of products into crates.

    Raises:
    - 400 Bad Request: If there is a ValueError during crate optimization.
    - 404 Not Found: If a product is not found in the database.
    - 500 Internal Server Error: If an unknown error occurs.
    """

    try:
        crate_optimzer = CrateOptimizer(order_products, data_provider)
        return crate_optimzer.calculate_optimal_crates()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except Exception:
        raise HTTPException(status_code=500, detail="Unknown error.")
