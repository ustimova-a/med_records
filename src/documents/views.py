import datetime

from fastapi import File
from fastapi import Form
from fastapi import Depends
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

import documents.schemas as doc_schemas
import documents.service as doc_service
import documents.models as doc_models

from users.models import User
from core.database import get_current_db
from users.service import get_current_user


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)


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
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> doc_schemas.Document:

    dest_path = await doc_service.upload_file(
        file=file,
        file_date=file_date
    )

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


@router.get("/{id_doc}", response_model=doc_schemas.Document)
async def get_document_by_id(
    *,
    id_doc: int,
    request: Request,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> doc_schemas.Document:

    result = await doc_models.Document.get_by_id(
        db_session=db_session,
        id=id_doc
    )
    file = await doc_service.get_file(
        request=request,
        url=result.source_doc_url
    )

    return result


@router.put("/{id_doc}/", response_model=doc_schemas.Document)
async def update_document(
    *,
    id_doc: int,
    doc_in: doc_schemas.Document,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> doc_schemas.Document:

    doc = await doc_models.Document.update(
        db_session=db_session,
        id=id_doc,
        cls_in=doc_in
    )
    return doc


@router.delete("/{id_doc}/")
async def delete_document(
    *,
    id_doc: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await doc_models.Document.delete(
        db_session=db_session,
        id=id_doc
    )
