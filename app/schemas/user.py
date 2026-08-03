from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    role: str 
    is_active: bool = True

class UserCreate(UserBase):
    user_id: str
    password_hash: str

class UserUpdate(BaseModel):
    username: str | None = None
    password_hash: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    is_active: bool | None = None

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    user_id: str
    created_at: datetime
