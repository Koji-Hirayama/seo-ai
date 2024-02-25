from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id:int
    email: str
    is_active: bool
    is_staff: bool
    created_at: datetime
    updated_at: datetime