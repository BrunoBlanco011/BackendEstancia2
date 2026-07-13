from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.core.security.auth import AuthService, Claims


class UserPrincipal:
    def __init__(self, user_id: int, email: str):
        self.user_id = user_id
        self.email = email


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserPrincipal:
    token = credentials.credentials

    claims = AuthService.validate_jwt(token)

    if claims is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado"
        )

    return UserPrincipal(user_id=claims.user_id, email=claims.email)


async def verify_token(request: Request) -> Optional[UserPrincipal]:
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.replace("Bearer ", "")
        claims = AuthService.validate_jwt(token)

        if claims is None:
            return None

        return UserPrincipal(user_id=claims.user_id, email=claims.email)
    except Exception:
        return None