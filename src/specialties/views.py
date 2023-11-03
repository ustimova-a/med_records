from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import specialties.schemas as sp_schemas
import specialties.models as sp_models


router = APIRouter(
    prefix="/specialties",
    tags=["specialties"]
)

# region SpecialtyCRUD


@router.get("/", response_model=List[sp_schemas.Specialty])
async def get_all_specialties(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[sp_schemas.Specialty]:

    specialties = await sp_models.Specialty.get_all(db_session=db_session)

    return specialties


@router.post("/", response_model=sp_schemas.Specialty)
async def create_specialty(
    *,
    specialty_in: sp_schemas.Specialty,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> sp_schemas.Specialty:

    specialty = await sp_models.Specialty.create(db_session=db_session, cls_in=specialty_in)
    return specialty


@router.get("/{specialty_id}/", response_model=sp_schemas.Specialty)
async def get_specialty_by_id(
    *,
    specialty_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> sp_schemas.Specialty:

    specialty = await sp_models.Specialty.get_by_id(db_session=db_session, id=specialty_id)
    return specialty


@router.put("/{specialty_id}/", response_model=sp_schemas.Specialty)
async def update_specialty(
    *,
    specialty_id: int,
    specialty_in: sp_schemas.Specialty,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> sp_schemas.Specialty:

    specialty = await sp_models.Specialty.update(
        db_session=db_session,
        id=specialty_id,
        cls_in=specialty_in
    )
    return specialty


@router.delete("/{specialty_id}/")
async def delete_specialty(
    *,
    specialty_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await sp_models.Specialty.delete(db_session=db_session, id=specialty_id)

# endregion
