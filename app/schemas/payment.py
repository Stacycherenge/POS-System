from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class PaymentBase(BaseModel):
    sale_id: str
    payment_method: str  
    amount_paid: Decimal

class PaymentCreate(PaymentBase):
    payment_id: str

class PaymentUpdate(BaseModel):
    sale_id: str | None = None
    payment_method: str | None = None
    amount_paid: Decimal | None = None

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    payment_id: str
