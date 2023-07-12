from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_current_db
from src.users.models import User
from src.users.service import get_current_user

import src.drugs.schemas as d_schemas
import src.drugs.models as d_models


router = APIRouter(
    prefix="/drugs",
    tags=["drugs"]
)

# region DrugCRUD


@router.get("/", response_model=List[d_schemas.Drug])
async def get_all_drugs(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[d_schemas.Drug]:

    drugs = await d_models.Drug.get_all(db_session=db_session)
    return drugs


@router.post("/", response_model=d_schemas.Drug)
async def create_drug(
    *,
    drug_in: d_schemas.Drug,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> d_schemas.Drug:

    drug = await d_models.Drug.create(db_session=db_session, cls_in=drug_in)
    return drug


@router.get("/{drug_id}/", response_model=d_schemas.Drug)
async def get_drug_by_id(
    *,
    drug_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> d_schemas.Drug:

    drug = await d_models.Drug.get_by_id(db_session=db_session, id=drug_id)
    return drug


@router.put("/{drug_id}/", response_model=d_schemas.Drug)
async def update_drug(
    *,
    drug_id: int,
    drug_in: d_schemas.Drug,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> d_schemas.Drug:

    drug = await d_models.Drug.update(
        db_session=db_session,
        id=drug_id,
        cls_in=drug_in
    )
    return drug


@router.delete("/{drug_id}/")
async def delete_drug(
    *,
    drug_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await d_models.Drug.delete(db_session=db_session, id=drug_id)

# endregion
