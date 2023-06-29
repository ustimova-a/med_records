import os
import jwt
import shutil

from fastapi import Depends
from fastapi import status
from fastapi import UploadFile
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError

from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config


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


async def get_file(request: Request) -> FileResponse:

    file = os.path.join(config.STORAGE_DIR, request.path_params['filename'])

    if not os.path.isfile(file):
        raise HTTPException(status_code=404, detail="File not found")

    media_type = None

    if request.query_params.get('download'):
        media_type = 'application/octet-stream'  # ?

    return FileResponse(file, media_type=media_type)


async def upload_file(
    file: UploadFile,
    db_session: AsyncSession
) -> dict:  # ?
    try:
        upload_dir = config.STORAGE_DIR
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        dest_path = os.path.join(upload_dir, file.filename)
        # logger.debug(dest_path)

        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        print(e)

    return dest_path
