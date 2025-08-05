# app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.utils.database import get_session
from app.auth.models.user_model import User
from app.auth.controller.user_controller import get_authenticated_user
from app.auth.schemas.user_schema import UserPublic

user_router = APIRouter(prefix="/users", tags=["Users"])

# 🧍 Obtener el usuario autenticado
@user_router.get("/me", response_model=UserPublic)
def read_current_user(authenticated_user: User = Depends(get_authenticated_user)):
    return authenticated_user

# 🔐 Obtener todos los usuarios (solo admin)
@user_router.get("/", response_model=list[UserPublic])
def read_all_users(
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    if authenticated_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso restringido a administradores."
        )
    users = db_session.exec(select(User)).all()
    return users

# 🗑️ Eliminar usuario por ID (solo admin)
@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def remove_user_by_id(
    user_id: int,
    db_session: Session = Depends(get_session),
    authenticated_user: User = Depends(get_authenticated_user)
):
    if authenticated_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar usuarios."
        )
    user_to_delete = db_session.get(User, user_id)
    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    db_session.delete(user_to_delete)
    db_session.commit()

    return {"message": f"Usuario con ID {user_id} eliminado correctamente."}
