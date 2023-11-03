from typing import List

from fastapi import Depends
from fastapi import Request
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import hospitals.schemas as h_schemas
import hospitals.models as h_models


router = APIRouter(
    prefix="/hospitals",
    tags=["hospitals"]
)

# region HospitalCRUD


@router.get("/", response_model=List[h_schemas.Hospital])
async def get_all_hospitals(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[h_schemas.Hospital]:

    hospitals = await h_models.Hospital.get_all(db_session=db_session)
    return hospitals


@router.post("/", response_model=h_schemas.Hospital)
async def create_hospital(
    *,
    hospital_in: h_schemas.Hospital,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> h_schemas.Hospital:

    hospital = await h_models.Hospital.create(db_session=db_session, cls_in=hospital_in)
    return hospital


@router.get("/{hospital_id}/", response_model=h_schemas.Hospital)
async def get_hospital_by_id(
    *,
    hospital_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> h_schemas.Hospital:

    hospital = await h_models.Hospital.get_by_id(db_session=db_session, id=hospital_id)
    return hospital


@router.put("/{hospital_id}/", response_model=h_schemas.Hospital)
async def update_hospital(
    *,
    hospital_id: int,
    hospital_in: h_schemas.Hospital,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> h_schemas.Hospital:

    hospital = await h_models.Hospital.update(
        db_session=db_session,
        id=hospital_id,
        cls_in=hospital_in
    )
    return hospital


@router.delete("/{hospital_id}/")
async def delete_hospital(
    *,
    hospital_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await h_models.Hospital.delete(db_session=db_session, id=hospital_id)

# endregion
