import secrets

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from cryptography.fernet import Fernet


security = HTTPBasic()
FERNET_KEY = b'09FPnNDxYMiYqEvHoyREPeA7c5Y5rEq9Y5wwZBPZVas='


def fernet_encrypt(message: str) -> str:
    b = Fernet(FERNET_KEY).encrypt(message.encode())
    return b.decode()


def fernet_decrypt(payload: str) -> str:
    b = Fernet(FERNET_KEY).decrypt(payload.encode())
    return b.decode()


async def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security)
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"admin"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
