from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    name: str
    brand: str
    product_price: Decimal
    stock_quantity: int
    expiry_date: str
    is_prescription_required: bool = False
    product_form: str  # tablet, syrup, capsule
    category_id: str
    supplier_id: int
    is_active: bool = True

class ProductCreate(ProductBase):
    product_id: str

class ProductUpdate(BaseModel):
    name: str | None = None
    brand: str | None = None
    product_price: Decimal | None = None
    stock_quantity: int | None = None
    expiry_date: str | None = None
    is_prescription_required: bool | None = None
    product_form: str | None = None
    category_id: str | None = None
    supplier_id: int | None = None
    is_active: bool | None = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    product_id: str
    created_at: datetime
