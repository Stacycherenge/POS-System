from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class SaleBase(BaseModel):
    user_id: str
    customer_id: str | None = None
    sale_date_time: str
    total_amount: Decimal
    sub_total: Decimal
    tax_amount: Decimal
    is_active: bool = True

class SaleCreate(SaleBase):
    sale_id: str

class SaleUpdate(BaseModel):
    user_id: str | None = None
    customer_id: str | None = None
    sale_date_time: str | None = None
    total_amount: Decimal | None = None
    sub_total: Decimal | None = None
    tax_amount: Decimal | None = None
    is_active: bool | None = None

class SaleRead(SaleBase):
    model_config = ConfigDict(from_attributes=True)
    sale_id: str
    created_at: datetime
