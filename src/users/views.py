from typing import List

from fastapi import Depends
from fastapi import Request
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import string_hash
from core.database import get_current_db
from documents.schemas import Document

import users.schemas as u_schemas
import users.service as u_service
import users.models as u_models


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# region UserCRUD


@router.get("/", response_model=List[u_schemas.UserRead])
async def get_all_users(
    *,
    request: Request,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> List[u_schemas.UserRead]:

    users = await u_models.User.get_all(db_session=db_session)

    # return src.app.templates.TemplateResponse(
    #     "get_all_users.html",
    #     {"request": request, "users": users}
    # )

    return users


@router.post("/", response_model=u_schemas.UserRead)
async def create_user(
    *,
    user_in: u_schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> u_models.User:

    if user_in.password:
        user_in.password = string_hash(user_in.password)

    user = await u_models.User.create(db_session=db_session, cls_in=user_in)
    return user


@router.get("/{user_id}/", response_model=u_schemas.UserRead)
async def get_user_by_id(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> u_models.User:

    user = await u_models.User.get_by_id(db_session=db_session, id=user_id)
    return user


@router.put("/{user_id}/", response_model=u_schemas.UserRead)
async def update_user(
    *,
    user_id: int,
    user_in: u_schemas.UserCreate,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> u_models.User:

    if user_in.password:
        user_in.password = string_hash(user_in.password)

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
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> u_schemas.UserRead:

    user = await u_models.User.delete(db_session=db_session, id=user_id)
    return user

# endregion


@router.get("/{user_id}/documents/", response_model=List[Document])
async def get_users_docs(
    *,
    user_id: int,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: u_models.User = Depends(u_service.get_current_user)
) -> List[Document]:

    result = await u_service.get_users_docs(
        user_id=user_id,
        db_session=db_session
    )
    return [Document(**jsonable_encoder(doc)) for doc in result]
