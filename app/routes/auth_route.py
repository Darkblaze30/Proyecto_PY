from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth.schemas.user_schema import UserCreate, UserLogin,UserPublic
from app.utils.database import get_session
from app.auth.models.user_model import User
from app.auth.controller.user_controller import handle_registration, handle_login

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserPublic)
def register_new_user(new_user: UserCreate, db_session: Session = Depends(get_session)):
    return handle_registration(new_user, db_session)

@auth_router.post("/login")
def authenticate_user(credentials: UserLogin, db_session: Session = Depends(get_session)):
    return handle_login(credentials, db_session)