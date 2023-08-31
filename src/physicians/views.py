from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import physicians.schemas as ph_schemas
import physicians.models as ph_models


router = APIRouter(
    prefix="/physicians",
    tags=["physicians"]
)

# region PhysicianCRUD


@router.get("/", response_model=List[ph_schemas.Physician])
async def get_all_physicians(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[ph_schemas.Physician]:

    physicians = await ph_models.Physician.get_all(db_session=db_session)
    return physicians


@router.post("/", response_model=ph_schemas.Physician)
async def create_physician(
    *,
    physician_in: ph_schemas.Physician,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> ph_schemas.Physician:

    physician = await ph_models.Physician.create(db_session=db_session, cls_in=physician_in)
    return physician


@router.get("/{physician_id}/", response_model=ph_schemas.Physician)
async def get_physician_by_id(
    *,
    physician_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> ph_schemas.Physician:

    physician = await ph_models.Physician.get_by_id(db_session=db_session, id=physician_id)
    return physician


@router.put("/{physician_id}/", response_model=ph_schemas.Physician)
async def update_physician(
    *,
    physician_id: int,
    physician_in: ph_schemas.Physician,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> ph_schemas.Physician:

    physician = await ph_models.Physician.update(
        db_session=db_session,
        id=physician_id,
        cls_in=physician_in
    )
    return physician


@router.delete("/{physician_id}/")
async def delete_physician(
    *,
    physician_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await ph_models.Physician.delete(db_session=db_session, id=physician_id)

# endregion
