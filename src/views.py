import os
import shutil

from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import APIRouter
from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config
import src.logger as logger
import src.schemas as schemas
import src.service as service
import src.security as security
import src.models.models as models

from src.database import get_current_db


router = APIRouter(dependencies=[Depends(security.get_current_username)])


@router.get("/")
async def login(username: str = Depends(security.get_current_username)):
    return {"username": username}


# region User

@router.get("/users", response_model=List[schemas.UserRead])
async def get_users_list(
    *,
    db_session: AsyncSession = Depends(get_current_db)
) -> List[models.User]:

    users = await models.User.get_all(db_session=db_session)
    print(users)
    return users

# endregion


# region Document

# @router.post("/users/{id_user}/documents")
# async def upload_document(
#     *,
#     doc: UploadFile,
#     db_session: AsyncSession = Depends(get_current_db)
# ) -> dict:  # ?

#     upload_dir = config.STORAGE_DIR
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)

#     dest_path = os.path.join(upload_dir, doc.filename)
#     # logger.debug(dest_path)

#     with open(dest_path, "wb") as buffer:
#         shutil.copyfileobj(doc.file, buffer)

#     return doc


@router.post("/users/{id_user}/documents", response_model=schemas.Document)
async def create_document(
    *,
    file: UploadFile,
    doc_in: schemas.Document,
    db_session: AsyncSession = Depends(get_current_db)
) -> models.Document:

    dest_path = await service.upload_file(file=file, db_session=db_session)
    print(dest_path)
    if 'source_doc_url' in doc_in.__dict__:
        doc_in.source_doc_url = dest_path

    doc_description = await models.Document.create(db_session=db_session, cls_in=doc_in)

    return doc_description

# endregion
