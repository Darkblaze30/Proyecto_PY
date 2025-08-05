from enum import Enum
from sqlmodel import SQLModel, Field



class UserRole(str, Enum):
    USER = "User"
    ADMIN = "Admin"

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    email_address: str = Field(index=True)
    hashed_password: str
    role: UserRole
