
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    category_name: str
    description: str | None = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    category_id: int 

class CategoryUpdate(BaseModel):
    category_name: str | None = None
    description: str | None = None
    is_active: bool | None = None

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    category_id: int  
    created_at: datetime
