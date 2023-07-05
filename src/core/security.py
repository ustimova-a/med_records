"""
Модуль безопасности для создания токенов пользователя и проверки паролей
"""
import uuid
import datetime

from typing import Any
from typing import Union

from jwt import encode as jwt_encode
from jwt import decode as jwt_decode

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

import src.core.config as config


SECRET_KEY = "42e126595ef550efbeaee5be8710bd1bf071b7e35fca7cfaa59699cfc1157c57"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24 * 30 * 3  # 90 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login/"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля из того что присылает пользователь в открытом виде и зашифрованный вид в базе данных
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_token(
    subject: Union[str, Any],
    expires_delta: datetime.timedelta = datetime.timedelta(
        days=config.get("Application", "Token", "Hours Live", fallback=10)
    )
) -> str:
    """
    Method creating access token.

    :param subject:
    :param expires_delta:
    :return:
    """
    expire = datetime.datetime.utcnow() + expires_delta

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "uuid": str(uuid.uuid4())
    }

    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(
    token: str
) -> Any:
    """
    Method decoding token.

    :param token:
    :return:
    """
    return jwt_decode(
        token, SECRET_KEY, algorithms=[ALGORITHM]
    )


def string_hash(string: str) -> str:
    """
    Method hashed string.

    :param string:
    :return:
    """
    return pwd_context.hash(string)

# security = HTTPBasic()
# FERNET_KEY = b'09FPnNDxYMiYqEvHoyREPeA7c5Y5rEq9Y5wwZBPZVas='


# def fernet_encrypt(message: str) -> str:
#     b = Fernet(FERNET_KEY).encrypt(message.encode())
#     return b.decode()


# def fernet_decrypt(payload: str) -> str:
#     b = Fernet(FERNET_KEY).decrypt(payload.encode())
#     return b.decode()


# async def get_current_username(
#     credentials: HTTPBasicCredentials = Depends(security)
# ):
#     current_username_bytes = credentials.username.encode("utf8")
#     correct_username_bytes = b"admin"
#     is_correct_username = secrets.compare_digest(
#         current_username_bytes, correct_username_bytes
#     )
#     current_password_bytes = credentials.password.encode("utf8")
#     correct_password_bytes = b"admin"
#     is_correct_password = secrets.compare_digest(
#         current_password_bytes, correct_password_bytes
#     )
#     if not (is_correct_username and is_correct_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Basic"},
#         )
#     return credentials.username
