from sqlmodel import SQLModel
from typing import Optional

class UserCreate(SQLModel):
    full_name: str
    email_address: str
    password: str
    role: str

class UserLogin(SQLModel):
    email_address: str
    password: str


class UserPublic(SQLModel):
    id: Optional[int]
    full_name: str
    email_address: str
    role: str
 