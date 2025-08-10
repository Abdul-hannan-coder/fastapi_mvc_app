from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ContactModel(BaseModel):
    id: Optional[str] = None  
    fname: str = Field(..., min_length=2, max_length=50)
    lname: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')
    address: str = Field(..., min_length=5, max_length=100)
    email: EmailStr
