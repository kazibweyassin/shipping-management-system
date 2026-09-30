from pydantic import BaseModel
from typing import List, Optional

class OrderCreate(BaseModel):
    customer_name: str
    destination: str
    weight_kg: float


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    destination: str
    weight_kg: float
    status: str

    class Config:
        from_attributes = True
    
class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    destination: Optional[str] = None
    weight_kg: Optional[float] = None