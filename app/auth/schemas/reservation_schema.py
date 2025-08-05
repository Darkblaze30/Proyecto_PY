from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ReservationCreate(BaseModel):
    room_id: int
    date_reservation: date
    start_time: time
    end_time: time

class ReservationUpdate(BaseModel):
    state: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    date_reservation: date
    start_time: time
    end_time: time
    state: str

    class Config:
        orm_mode = True