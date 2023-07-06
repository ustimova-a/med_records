import datetime

from typing import List
from typing import Optional

from fastapi import File
from fastapi import Form
from fastapi import Depends
from fastapi import status
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

import src.core.config as config
import src.core.schemas as schemas
import src.core.service as service
import src.core.security as security
import src.core.models.models as models

from src.core.logger import logger
from src.core.database import get_current_db


# router = APIRouter(dependencies=[Depends(security.get_current_username)])
router = APIRouter(
    prefix="",
    tags=["core"]
)


# @router.get("/")
# async def login(username: str = Depends(security.get_current_username)):
#     return {"username": username}
