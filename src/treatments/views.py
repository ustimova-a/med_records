from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import treatments.schemas as tr_schemas
import treatments.models as tr_models


router = APIRouter(
    prefix="/treatments",
    tags=["treatments"]
)

# region TreatmentCRUD


@router.get("/", response_model=List[tr_schemas.Treatment])
async def get_all_treatments(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[tr_schemas.Treatment]:

    treatments = await tr_models.Treatment.get_all(db_session=db_session)
    return treatments


@router.post("/", response_model=tr_schemas.Treatment)
async def create_treatment(
    *,
    treatment_in: tr_schemas.Treatment,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> tr_schemas.Treatment:

    treatment = await tr_models.Treatment.create(db_session=db_session, cls_in=treatment_in)
    return treatment


@router.get("/{treatment_id}/", response_model=tr_schemas.Treatment)
async def get_treatment_by_id(
    *,
    treatment_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> tr_schemas.Treatment:

    treatment = await tr_models.Treatment.get_by_id(db_session=db_session, id=treatment_id)
    return treatment


@router.put("/{treatment_id}/", response_model=tr_schemas.Treatment)
async def update_treatment(
    *,
    treatment_id: int,
    treatment_in: tr_schemas.Treatment,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> tr_schemas.Treatment:

    treatment = await tr_models.Treatment.update(
        db_session=db_session,
        id=treatment_id,
        cls_in=treatment_in
    )
    return treatment


@router.delete("/{treatment_id}/")
async def delete_treatment(
    *,
    treatment_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await tr_models.Treatment.delete(db_session=db_session, id=treatment_id)

# endregion
