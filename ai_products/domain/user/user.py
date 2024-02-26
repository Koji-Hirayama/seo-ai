from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id:int | None = None
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    last_login: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None