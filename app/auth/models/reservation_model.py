from sqlmodel import SQLModel,Field,Relationship
from datetime import date, time
from enum import Enum
from typing import Optional
from app.auth.models.user_model import User
from app.auth.models.room_model import Room

class State(Enum):
    pending = 'Pending'
    confirm = 'Confirm'
    canceled = 'Canceled'


class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    user_id: int = Field(foreign_key="user.id")
    room_id: int = Field(foreign_key="room.id")
    
    date_reservation: date
    start_time: time
    end_time: time
    state: State

    user: Optional["User"] = Relationship()
    room: Optional["Room"] = Relationship()


