from sqlmodel import SQLModel, Field,Column
from sqlalchemy import JSON
from typing import List

class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    capacity: int
    utilities: List[str] = Field(default=[], sa_column=Column(JSON))
