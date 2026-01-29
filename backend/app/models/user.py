from pydantic import BaseModel

class UserStatus(BaseModel):
    device_id: str
    is_premium: bool
    daily_count: int
    limit: int

class PurchaseRequest(BaseModel):
    device_id: str
