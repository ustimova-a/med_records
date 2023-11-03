from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_current_db
from users.models import User
from users.service import get_current_user

import side_effects.schemas as se_schemas
import side_effects.models as se_models


router = APIRouter(
    prefix="/side_effects",
    tags=["side_effects"]
)

# region SideEffectCRUD


@router.get("/", response_model=List[se_schemas.SideEffect])
async def get_all_side_effects(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[se_schemas.SideEffect]:

    side_effects = await se_models.SideEffect.get_all(db_session=db_session)
    return side_effects


@router.post("/", response_model=se_schemas.SideEffect)
async def create_side_effect(
    *,
    se_in: se_schemas.SideEffect,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> se_schemas.SideEffect:

    side_effect = await se_models.SideEffect.create(db_session=db_session, cls_in=se_in)
    return side_effect


@router.get("/{se_id}/", response_model=se_schemas.SideEffect)
async def get_side_effect_by_id(
    *,
    se_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> se_schemas.SideEffect:

    side_effect = await se_models.SideEffect.get_by_id(db_session=db_session, id=se_id)
    return side_effect


@router.put("/{se_id}/", response_model=se_schemas.SideEffect)
async def update_side_effect(
    *,
    se_id: int,
    se_in: se_schemas.SideEffect,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> se_schemas.SideEffect:

    side_effect = await se_models.SideEffect.update(
        db_session=db_session,
        id=se_id,
        cls_in=se_in
    )
    return side_effect


@router.delete("/{se_id}/")
async def delete_side_effect(
    *,
    se_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await se_models.SideEffect.delete(db_session=db_session, id=se_id)

# endregion
