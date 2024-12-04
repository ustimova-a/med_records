"""
Модуль безопасности для создания токенов пользователя и проверки паролей
"""
import uuid
import jwt
import bcrypt
import datetime

from typing import Any
from typing import Union

from fastapi.security import OAuth2PasswordBearer

import core.config as config


SECRET_KEY = config.JWT_KEY
ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_HOURS = 24 * 30 * 3  # 90 days

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля из того что присылает пользователь в открытом виде и зашифрованный вид в базе данных
    :param plain_password:
    :param hashed_password:
    :return:
    """
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def create_token(
    subject: Union[str, Any],
    expires_delta: datetime.timedelta = datetime.timedelta(
        days=config.TOKEN_EXPIRATION_DAYS
    )
) -> str:
    """
    Method creating access token.

    :param subject:
    :param expires_delta:
    :return:
    """
    expire = datetime.datetime.now() + expires_delta

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "uuid": str(uuid.uuid4())
    }

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(
    token: str
) -> Any:
    """
    Method decoding token.

    :param token:
    :return:
    """
    return jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM]
    )


def hash_password(password: str) -> str:
    """
    Method hashed password.

    :param string:
    :return:
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_password = hashed_password.decode('utf-8')
    return string_password

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
