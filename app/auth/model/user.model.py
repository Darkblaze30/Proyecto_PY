from enum import Enum
from sqlmodel import SQLModel, Field

class Rol(Enum):
    user = 'User',
    admin = 'Admin'

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    password: str 
    rol: Rol