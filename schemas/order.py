from pydantic import BaseModel

class ProductOrder(BaseModel):
    id: str
    orderId: str
    sku: str
    unitCount: int


class CrateCounts(BaseModel):
    Supplier: int
    Slot6: int
    Slot12: int
    Slot20: int
