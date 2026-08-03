from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class SaleItemBase(BaseModel):
    sale_id: str
    product_id: str
    quantity_sold: int
    price_at_sale: Decimal

class SaleItemCreate(SaleItemBase):
    sale_item_id: str

class SaleItemUpdate(BaseModel):
    sale_id: str | None = None
    product_id: str | None = None
    quantity_sold: int | None = None
    price_at_sale: Decimal | None = None

class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)
    sale_item_id: str
