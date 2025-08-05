# app/routes/room_routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from app.utils.database import get_session
from app.auth.models.user_model import User
from app.auth.models.room_model import Room
from app.auth.controller.user_controller import get_authenticated_user
from app.auth.schemas.room_schema import RoomCreate, RoomResponse, RoomUpdate
from app.auth.controller.room_controller import create_room

room_router = APIRouter(prefix="/rooms", tags=["Rooms"])

# 👀 Ver todas las salas (acceso público)
@room_router.get("/", response_model=List[RoomResponse])
def read_all_rooms(db_session: Session = Depends(get_session)):
    rooms = db_session.exec(select(Room)).all()
    return rooms

# 🏗️ Crear sala (solo admin)
@room_router.post("/", response_model=RoomResponse)
def create_new_room(
    room_data: RoomCreate,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    if authenticated_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear salas."
        )
    return create_room(db_session, room_data)

# 🛠️ Actualizar sala por ID (solo admin)
@room_router.put("/{room_id}", response_model=RoomResponse)
def update_room_by_id(
    room_id: int,
    room_data: RoomUpdate,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    if authenticated_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar salas."
        )

    room = db_session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada.")

    for key, value in room_data.dict(exclude_unset=True).items():
        setattr(room, key, value)

    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)
    return room

# 🗑️ Eliminar sala por ID (solo admin)
@room_router.delete("/{room_id}", response_model=RoomResponse)
def delete_room_by_id(
    room_id: int,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    if authenticated_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar salas."
        )

    room = db_session.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala no encontrada.")

    db_session.delete(room)
    db_session.commit()
    return room