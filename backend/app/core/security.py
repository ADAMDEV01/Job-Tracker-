from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET

password_hash = PasswordHash.recommended()
ALGORITHM = "HS256"
DUMMY_PASSWORD_HASH = password_hash.hash("invalid-login-placeholder")


class JWTConfigurationError(RuntimeError):
    pass


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    secret = _get_jwt_secret()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, object]:
    return jwt.decode(
        token,
        _get_jwt_secret(),
        algorithms=[ALGORITHM],
        options={"require": ["exp", "sub"]},
    )


def _get_jwt_secret() -> str:
    if JWT_SECRET is None or len(JWT_SECRET.encode("utf-8")) < 32:
        raise JWTConfigurationError(
            "JWT_SECRET must be set to a random value of at least 32 bytes."
        )
    return JWT_SECRET
