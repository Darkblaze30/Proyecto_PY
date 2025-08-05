from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import timedelta, date, datetime
from app.auth.models.reservation_model import Reservation, State
from app.auth.schemas.reservation_schema import ReservationCreate
from app.auth.models.user_model import User

def create_reservation(
    session: Session,
    reservation_data: ReservationCreate,
    current_user: User
) -> Reservation:

    duration = datetime.combine(date.min, reservation_data.end_time) - datetime.combine(date.min, reservation_data.start_time)
    if duration < timedelta(hours=1):
        raise HTTPException(status_code=400, detail="La reserva debe durar al menos 1 hora.")

    # Validación: bloques exactos de 1 hora
    if duration.total_seconds() % 3600 != 0:
        raise HTTPException(status_code=400, detail="La reserva debe ser en bloques exactos de 1 hora.")

    overlapping_reservations = session.exec(
        select(Reservation).where(
            Reservation.room_id == reservation_data.room_id,
            Reservation.date_reservation == reservation_data.date_reservation,
            Reservation.state != State.canceled,
            Reservation.start_time < reservation_data.end_time,
            Reservation.end_time > reservation_data.start_time
        )
    ).all()

    if overlapping_reservations:
        raise HTTPException(status_code=409, detail="Ya existe una reserva en ese horario para esta sala.")

    new_reservation = Reservation(
        user_id=current_user.id,
        room_id=reservation_data.room_id,
        date_reservation=reservation_data.date_reservation,
        start_time=reservation_data.start_time,
        end_time=reservation_data.end_time,
        state=State.pending
    )

    session.add(new_reservation)
    session.commit()
    session.refresh(new_reservation)

    return new_reservation