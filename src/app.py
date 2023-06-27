import uvicorn

from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config
import src.schemas as schemas
import src.service as service
import src.security as security
import src.models.models as models

from src.views import router
from src.database import get_current_db

app = FastAPI()

# app.mount("/", StaticFiles(directory=config.STATIC_DIR), name="app")

app.add_route('/storage/{filename:path}', service.get_file, ['GET'])

app.include_router(router)


if __name__ == "__main__":
    server_config = uvicorn.Config("app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
