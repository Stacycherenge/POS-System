from pydantic import BaseModel, ConfigDict

class ReceiptBase(BaseModel):
    sale_id: str
    receipt_number: str
    issued_date_time: str

class ReceiptCreate(ReceiptBase):
    receipt_id: str

class ReceiptUpdate(BaseModel):
    sale_id: str | None = None
    receipt_number: str | None = None
    issued_date_time: str | None = None

class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)
    receipt_id: str
