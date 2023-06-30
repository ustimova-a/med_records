import uvicorn

from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config
import src.schemas as schemas
import src.service as service
import src.security as security
import src.models.models as models

from src.views import router
from src.database import get_current_db

app = FastAPI()

# Workaround to debug `422 Unprocessable Entity` error
# import logging


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    print(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
# workaround end

# app.mount("/", StaticFiles(directory=config.STATIC_DIR), name="app")

app.add_route('/storage/{filename:path}', service.get_file, ['GET'])

app.include_router(router)


if __name__ == "__main__":
    server_config = uvicorn.Config("app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
