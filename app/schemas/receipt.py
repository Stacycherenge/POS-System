from pydantic import BaseModel, ConfigDict

class ReceiptBase(BaseModel):
    sale_id: int
    receipt_number: str
    issued_date_time: str

class ReceiptCreate(ReceiptBase):
    receipt_id: int

class ReceiptUpdate(BaseModel):
    sale_id: int | None = None
    receipt_number: str | None = None
    issued_date_time: str | None = None

class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)
    receipt_id: int
