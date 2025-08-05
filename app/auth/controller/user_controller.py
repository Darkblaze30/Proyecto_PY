from fastapi import HTTPException, status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.auth.schemas.user_schema import UserCreate, UserLogin
from app.auth.models.user_model import User
from app.utils.security import generate_access_token, verify_access_token
from app.utils.database import get_session

# 🔐 Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 📝 Registro de usuario
def handle_registration(user_data: UserCreate, session: Session) -> User:
    # Verificar si el email ya está registrado
    existing_user = session.exec(
        select(User).where(User.email_address == user_data.email_address)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado."
        )

    # Crear nuevo usuario con contraseña hasheada
    new_user = User(
        full_name=user_data.full_name,
        email_address=user_data.email_address,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 🔐 Autenticación de usuario
def handle_login(login_data: UserLogin, session: Session):
    # Buscar usuario por email
    user = session.exec(
        select(User).where(User.email_address == login_data.email_address)
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas."
        )

    # Generar token JWT
    token_payload = {
        "sub": str(user.id),
        "email": user.email_address,
        "role": user.role
    }

    access_token = generate_access_token(token_payload)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_authenticated_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado."
        )

    user_id = int(payload.get("sub"))
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    return user
