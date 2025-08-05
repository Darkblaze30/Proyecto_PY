from sqlmodel import Session
from app.auth.models.room_model import Room
from app.auth.schemas.room_schema import RoomCreate

def create_room(session: Session, room_data: RoomCreate) -> Room:
    new_room = Room(
        name=room_data.name,
        headquarters=room_data.headquarters,
        capacity=room_data.capacity,
        utilities=room_data.utilities
    )
    session.add(new_room)
    session.commit()
    session.refresh(new_room)
    return new_room