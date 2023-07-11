"""
Model authorization view.

Author: exrofol
"""
from typing import Any
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from src.users.service import get_current_user

from src.database import get_current_db
from src.security import verify_password
from src.core.auth import schemas as auth_schemas

from src.users.models import User
from src.users.models import Session


router = APIRouter(tags=["auth"])


@router.post("/login/", response_model=auth_schemas.Token)
async def login(
    *,
    request: Request,
    db_session: AsyncSession = Depends(get_current_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Метод авторизации на сервере.

    Возвращает токен.
    """
    user = await User.get_user_by_login(
        session=db_session,
        login=form_data.username
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    user_session = await Session.create(
        db_session=db_session,
        user=user,
        user_agent=request.headers.get('user-agent', 'Unknown')
    )

    return auth_schemas.Token(
        access_token=user_session.token
    )


@router.post("/logout/")
async def logout(
    *,
    db_session: AsyncSession = Depends(get_current_db),
    current_user: User = Depends(get_current_user),
    request: Request
) -> Any:
    """
    Метод логаута с сервера.

    Деактивирует токен.
    """
    authorization: Union[str, None] = request.headers.get(
        "Authorization",
        default=None
    )

    if authorization:
        scheme, _, param = authorization.partition(" ")
        if scheme.lower() == 'bearer':
            session = await Session.get_by_token(
                db_session=db_session,
                token=param
            )
            if session:
                await session.set_expired(db_session=db_session)

    return Response(status_code=200)
