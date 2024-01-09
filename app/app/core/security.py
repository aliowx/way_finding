from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app import exceptions as exc
from app.core.config import settings
from app.utils import MessageCodes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class JWTHandler:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    @staticmethod
    def encode(payload: dict[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.access_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def encode_refresh_token(payload: dict[str, Any]) -> str:
        expire = datetime.utcnow() + timedelta(minutes=JWTHandler.refresh_token_expire)
        payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            result: dict = jwt.decode(
                token, JWTHandler.secret_key, algorithms=[JWTHandler.algorithm]
            )
            exp = result.get("exp")
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise exc.InternalErrorException(
                    detail="Token expired",
                    msg_code=MessageCodes.expired_token,
                )
            return result
        except jwt.ExpiredSignatureError:
            raise exc.InternalErrorException(
                detail="Token expired",
                msg_code=MessageCodes.expired_token,
            )
        except jwt.InvalidTokenError:
            raise exc.InternalErrorException(
                detail="Invalid token",
                msg_code=MessageCodes.invalid_token,
            )

    @staticmethod
    def decode_expired(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except jwt.InvalidTokenError:
            raise exc.InternalErrorException(
                detail="Invalid token",
                msg_code=MessageCodes.invalid_token,
            )

    @staticmethod
    def token_expiration(token: str) -> datetime | None:
        try:
            decoded_token = jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": True},
            )
            exp = decoded_token.get("exp")
            if exp:
                return datetime.fromtimestamp(exp).replace(tzinfo=timezone.utc)
            return None
        except jwt.ExpiredSignatureError:
            raise exc.InternalErrorException(
                detail="Token expired",
                msg_code=MessageCodes.expired_token,
            )
        except jwt.InvalidTokenError:
            raise exc.InternalErrorException(
                detail="Invalid token",
                msg_code=MessageCodes.invalid_token,
            )
