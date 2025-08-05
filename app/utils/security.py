from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

KeySecret = os.getenv('KEY_SECRET')
JwtAlgorithm = os.getenv('JWT_ALGORITHM')
TokenExpiryMinutes = int(os.getenv('TOKEN_EXPIRY_MINUTES', 30))

def generate_access_token(payload_data: dict) -> str:
    token_data = payload_data.copy()
    expiration_time = datetime.utcnow() + timedelta(minutes=TokenExpiryMinutes)
    token_data.update({"exp": expiration_time})
    jwt_token = jwt.encode(token_data, KeySecret, algorithm=JwtAlgorithm)
    return jwt_token

def verify_access_token(token: str) -> dict | None:
    try:
        decoded_payload = jwt.decode(token, KeySecret, algorithms=[JwtAlgorithm])
        return decoded_payload
    except JWTError:
        return None