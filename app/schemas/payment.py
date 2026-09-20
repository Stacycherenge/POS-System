from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class PaymentBase(BaseModel):
    sale_id: int
    payment_method: str  
    amount_paid: Decimal

class PaymentCreate(PaymentBase):
    payment_id: int

class PaymentUpdate(BaseModel):
    sale_id: int | None = None
    payment_method: str | None = None
    amount_paid: Decimal | None = None

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    payment_id: int
