from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from datetime import date
from app.utils.database import get_session
from app.auth.models.reservation_model import Reservation
from app.auth.models.user_model import User
from app.auth.controller.user_controller import get_authenticated_user
from app.auth.schemas.reservation_schema import ReservationCreate, ReservationResponse
from app.auth.controller.reservation_controller import create_reservation

reservation_router = APIRouter(prefix="/reservations", tags=["Reservations"])

@reservation_router.post("/", response_model=ReservationResponse)
def create_new_reservation(
    reservation_data: ReservationCreate,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    return create_reservation(db_session, reservation_data, authenticated_user)

@reservation_router.get("/me", response_model=List[ReservationResponse])
def read_my_reservations(
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    reservations = db_session.exec(
        select(Reservation).where(Reservation.user_id == authenticated_user.id)
    ).all()

    if not reservations:
        raise HTTPException(status_code=404, detail="No se encontraron reservas para este usuario.")
    return reservations

@reservation_router.get("/room/{room_id}", response_model=List[ReservationResponse])
def read_reservations_by_room(
    room_id: int,
    db_session: Session = Depends(get_session)
):
    reservations = db_session.exec(
        select(Reservation).where(Reservation.room_id == room_id)
    ).all()

    if not reservations:
        raise HTTPException(status_code=404, detail="No se encontraron reservas para esta sala.")
    return reservations

@reservation_router.get("/date/{reservation_date}", response_model=List[ReservationResponse])
def read_reservations_by_date(
    reservation_date: date,
    db_session: Session = Depends(get_session)
):
    reservations = db_session.exec(
        select(Reservation).where(Reservation.date_reservation == reservation_date)
    ).all()

    if not reservations:
        raise HTTPException(status_code=404, detail="No se encontraron reservas para esa fecha.")
    return reservations

@reservation_router.delete("/{reservation_id}", response_model=dict)
def cancel_reservation_by_id(
    reservation_id: int,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    reservation = db_session.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")

    if reservation.user_id != authenticated_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva.")

    reservation.state = "Canceled"
    db_session.commit()

    return {"message": f"Reserva con ID {reservation_id} cancelada correctamente."}