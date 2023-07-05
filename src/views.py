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
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

import src.core.config as config
import src.schemas as schemas
import src.service as service
import src.core.security as security
import src.models.models as models

from src.core.logger import logger
from src.core.database import get_current_db


# router = APIRouter(dependencies=[Depends(security.get_current_username)])
router = APIRouter()


# @router.get("/")
# async def login(username: str = Depends(security.get_current_username)):
#     return {"username": username}


# region User

@router.get("/users/", response_model=List[schemas.UserRead])
async def get_all_users(
    *,
    db_session: AsyncSession = Depends(get_current_db)
) -> List[models.User]:

    users = await models.User.get_all(db_session=db_session)

    return users


@router.post("/users/", response_model=schemas.UserRead)
async def create_user(
    *,
    user_in: schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db)
) -> models.User:

    user = await models.User.create(db_session=db_session, cls_in=user_in)
    return user


@router.get("/users/{user_id}/", response_model=schemas.UserRead)
async def get_user_by_id(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db)
) -> models.User:

    user = await models.User.get_by_id(db_session=db_session, id=user_id)
    return user


@router.put("/users/{user_id}/", response_model=schemas.UserRead)
async def update_user(
    *,
    user_id: int,
    user_in: schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db)
) -> models.User:

    user = await models.User.update(
        db_session=db_session,
        id=user_id,
        cls_in=user_in
    )
    return user


@router.delete("/users/{user_id}/")
async def delete_user(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db)
) -> models.User:

    user = await models.User.delete(db_session=db_session, id=user_id)
    return user

# endregion


# region Document

@router.post("/users/{id_user}/documents/", response_model=schemas.Document)
async def create_document(
    *,
    id_user: int,
    file: UploadFile = File(),
    file_date: str = Form(example='dd.mm.yyyy'),
    # physician_id: Optional[int] = Form(),
    # hospital_id: Optional[int] = Form(),
    # condition_id: Optional[int] = Form(),
    # treatment_id: Optional[int] = Form(),
    db_session: AsyncSession = Depends(get_current_db)
) -> schemas.Document:

    dest_path = await service.upload_file(file=file)

    doc_in = schemas.Document(
        date=datetime.datetime.strptime(file_date, '%d.%m.%Y'),
        user_id=id_user,
        source_doc_url=dest_path,
        # physician_id=physician_id,
        # hospital_id=hospital_id,
        # condition_id=condition_id,
        # treatment_id=treatment_id
    )
    doc_description = await models.Document.create(
        db_session=db_session,
        cls_in=doc_in
    )

    return schemas.Document(**jsonable_encoder(doc_description))

# endregion
