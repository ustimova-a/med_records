import os

from typing import Any

from fastapi import UploadFile
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

import core.config as config
from core.logger import logger


async def get_file(
    request: Request,
    url: str
) -> FileResponse:

    request.path_params['filename'] = url
    file = os.path.join(request.path_params['filename'])

    if not os.path.isfile(file):
        raise HTTPException(status_code=404, detail="File not found")

    media_type = None

    if request.query_params.get('download'):
        media_type = 'application/octet-stream'

    return FileResponse(file, media_type=media_type)


async def upload_file(
    file: UploadFile,
    file_date: str
) -> Any:
    try:
        upload_dir = config.STORAGE_DIR
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        dest_path = os.path.join(upload_dir, f'{file_date}.{file.filename}')
        logger.debug(f'File stored at: {dest_path}')

        with open(dest_path, "wb") as f:
            f.write(await file.read())
            # shutil.copyfileobj(file.file, buffer)
        logger.debug(f'File uploaded: {file.filename}')

    except Exception as e:
        logger.error(e)
    # except (UniqueViolationError, IntegrityError) as e:
    #     logger.error(f'File with such name already exists: {e}')

    return dest_path
