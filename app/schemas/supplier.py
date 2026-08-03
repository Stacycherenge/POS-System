from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SupplierBase(BaseModel):
    company_name: str
    contact_name: str
    phone_number: str
    email: str
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    company_name: str | None = None
    contact_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    is_active: bool | None = None

class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    supplier_id: int
    created_at: datetime
