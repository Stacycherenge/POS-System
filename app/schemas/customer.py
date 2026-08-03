from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CustomerBase(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    phone_number: str
    date_of_birth: str
    is_active: bool = True

class CustomerCreate(CustomerBase):
    customer_id: str

class CustomerUpdate(BaseModel):
    user_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    date_of_birth: str | None = None
    is_active: bool | None = None

class CustomerRead(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    customer_id: str
    created_at: datetime
