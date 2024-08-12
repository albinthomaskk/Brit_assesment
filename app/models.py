from pydantic import BaseModel
from typing import Optional, List

class LoginData(BaseModel):
    username: str
    password: str

class CartItem(BaseModel):
    fruit_id: str
    quantity: int

class AddToCartRequest(BaseModel):
    items: List[CartItem]

class UserCreate(BaseModel):
    username: str
    password: str