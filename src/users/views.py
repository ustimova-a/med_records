from typing import List

from fastapi import Depends
from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession

import src.security as security
import src.core.config as config
import src.users.schemas as u_schemas
import src.users.service as u_service
import src.users.models as u_models

from src.app import templates
from src.logger import logger
from src.database import get_current_db


# router = APIRouter(dependencies=[Depends(security.get_current_username)])
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# region User


@router.get("/", response_class=HTMLResponse)
async def get_all_users(
    *,
    request: Request,
    db_session: AsyncSession = Depends(get_current_db)
) -> HTMLResponse:

    users = await u_models.User.get_all(db_session=db_session)

    # template = template_env.get_template("get_all_users.html")
    # template.render(users=users)

    # return HTMLResponse(content=html_content, status_code=200)
    return templates.TemplateResponse(
        "get_all_users.html",
        {"request": request, "users": users}
    )


@router.post("/", response_model=u_schemas.UserRead)
async def create_user(
    *,
    user_in: u_schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db)
) -> u_models.User:

    user = await u_models.User.create(db_session=db_session, cls_in=user_in)
    return user


@router.get("/{user_id}/", response_model=u_schemas.UserRead)
async def get_user_by_id(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db)
) -> u_models.User:

    user = await u_models.User.get_by_id(db_session=db_session, id=user_id)
    return user


@router.put("/{user_id}/", response_model=u_schemas.UserRead)
async def update_user(
    *,
    user_id: int,
    user_in: u_schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db)
) -> u_models.User:

    user = await u_models.User.update(
        db_session=db_session,
        id=user_id,
        cls_in=user_in
    )
    return user


@router.delete("/{user_id}/")
async def delete_user(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db)
) -> u_models.User:

    user = await u_models.User.delete(db_session=db_session, id=user_id)
    return user

# endregion
