import datetime

from fastapi import File
from fastapi import Form
from fastapi import Depends
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

import src.core.config as config
import src.documents.schemas as doc_schemas
import src.documents.service as doc_service
import src.documents.models as doc_models

from src.core.logger import logger
from src.core.database import get_current_db


# router = APIRouter(dependencies=[Depends(security.get_current_username)])
router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


# region Document

@router.post("/", response_model=doc_schemas.Document)
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
) -> doc_schemas.Document:

    dest_path = await doc_service.upload_file(file=file, file_date=file_date)

    doc_in = doc_schemas.Document(
        date=datetime.datetime.strptime(file_date, '%d.%m.%Y'),
        user_id=id_user,
        source_doc_url=dest_path,
        # physician_id=physician_id,
        # hospital_id=hospital_id,
        # condition_id=condition_id,
        # treatment_id=treatment_id
    )
    doc_description = await doc_models.Document.create(
        db_session=db_session,
        cls_in=doc_in
    )

    return doc_schemas.Document(**jsonable_encoder(doc_description))

# endregion
