import os
import shutil

from fastapi import UploadFile
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config


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
