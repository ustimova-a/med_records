from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import conditions.schemas as cond_schemas
import conditions.models as cond_models


router = APIRouter(
    prefix="/conditions",
    tags=["conditions"]
)

# region ConditionCRUD


@router.get("/", response_model=List[cond_schemas.Condition])
async def get_all_condition(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[cond_schemas.Condition]:

    conditions = await cond_models.Condition.get_all(db_session=db_session)

    return conditions


@router.post("/", response_model=cond_schemas.Condition)
async def create_condition(
    *,
    visit_in: cond_schemas.Condition,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> cond_schemas.Condition:

    condition = await cond_models.Condition.create(db_session=db_session, cls_in=visit_in)
    return condition


@router.get("/{cond_id}/", response_model=cond_schemas.Condition)
async def get_condition_by_id(
    *,
    cond_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> cond_schemas.Condition:

    condition = await cond_models.Condition.get_by_id(db_session=db_session, id=cond_id)
    return condition


@router.put("/{cond_id}/", response_model=cond_schemas.Condition)
async def update_condition(
    *,
    cond_id: int,
    cond_in: cond_schemas.Condition,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> cond_schemas.Condition:

    condition = await cond_models.Condition.update(
        db_session=db_session,
        id=cond_id,
        cls_in=cond_in
    )
    return condition


@router.delete("/{cond_id}/")
async def delete_condition(
    *,
    cond_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await cond_models.Condition.delete(db_session=db_session, id=cond_id)

# endregion
