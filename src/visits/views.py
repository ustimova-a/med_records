from typing import List

from fastapi import Depends
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_current_db
from src.users.models import User
from src.users.service import get_current_user

import src.visits.schemas as v_schemas
import src.visits.models as v_models


router = APIRouter(
    prefix="/visits",
    tags=["visits"]
)

# region VisitCRUD


@router.get("/", response_model=List[v_schemas.Visit])
async def get_all_visits(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> List[v_schemas.Visit]:

    visits = await v_models.Visit.get_all(db_session=db_session)
    return visits


@router.post("/", response_model=v_schemas.Visit)
async def create_visit(
    *,
    visit_in: v_schemas.Visit,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> v_schemas.Visit:

    visit = await v_models.Visit.create(db_session=db_session, cls_in=visit_in)
    return visit


@router.get("/{visit_id}/", response_model=v_schemas.Visit)
async def get_visit_by_id(
    *,
    visit_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> v_schemas.Visit:

    visit = await v_models.Visit.get_by_id(db_session=db_session, id=visit_id)
    return visit


@router.put("/{visit_id}/", response_model=v_schemas.Visit)
async def update_visit(
    *,
    visit_id: int,
    visit_in: v_schemas.Visit,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> v_schemas.Visit:

    visit = await v_models.Visit.update(
        db_session=db_session,
        id=visit_id,
        cls_in=visit_in
    )
    return visit


@router.delete("/{visit_id}/")
async def delete_visit(
    *,
    visit_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user)
) -> None:

    await v_models.Visit.delete(db_session=db_session, id=visit_id)

# endregion
