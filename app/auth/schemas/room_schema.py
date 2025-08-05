from pydantic import BaseModel
from typing import List, Optional

class RoomCreate(BaseModel):
    name: str
    headquarters: str
    capacity: int
    utilities: List[str] = []

class RoomUpdate(BaseModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None
    capacity: Optional[int] = None
    utilities: Optional[List[str]] = None

class RoomResponse(BaseModel):
    id: int
    name: str
    headquarters: str
    capacity: int
    utilities: List[str]

    class Config:
        orm_mode = True