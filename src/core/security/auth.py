import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()


class Claims:
    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = email


class AuthService:
    JWT_SECRET = os.getenv("JWT_SECRET", "AmethToledo")
    EXPIRATION_TIME = 24 * 60 * 60 * 1000
    ALGORITHM = "HS256"

    @staticmethod
    def generate_jwt(user_id: int, email: str) -> str:
        expiration_time = datetime.utcnow() + timedelta(milliseconds=AuthService.EXPIRATION_TIME)

        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expiration_time
        }

        token = jwt.encode(payload, AuthService.JWT_SECRET, algorithm=AuthService.ALGORITHM)
        return token

    @staticmethod
    def validate_jwt(token_string: str) -> Optional[Claims]:
        try:
            decoded = jwt.decode(token_string, AuthService.JWT_SECRET, algorithms=[AuthService.ALGORITHM])
            return Claims(
                user_id=decoded.get("user_id"),
                email=decoded.get("email")
            )
        except JWTError:
            return None
        except Exception:
            return None