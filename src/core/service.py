import os
import jwt
import shutil
import datetime

from typing import Any

from fastapi import Depends
from fastapi import status
from fastapi import UploadFile
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

import src.core.config as config
from src.logger import logger


# async def get_current_user(
#     db_session: AsyncSession = Depends(get_db),
#     token: str = Depends(reusable_oauth2)
# ) -> User:
#     try:
#         payload = jwt.decode(
#             token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         token_data = TokenPayload(**payload)

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(  # pylint: disable=raise-missing-from
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token is expired"
#         )
#     except jwt.PyJWTError:
#         raise HTTPException(  # pylint: disable=raise-missing-from
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Unauthorized"
#         )
#     except ValidationError:
#         raise HTTPException(  # pylint: disable=raise-missing-from
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials"
#         )

#     user = await user_get_by_id(
#         db_session=db_session,
#         user_id=token_data.sub
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )
#     return user
