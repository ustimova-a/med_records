import jwt
import time

from typing import List

from fastapi import Depends
from fastapi.exceptions import HTTPException

from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic.error_wrappers import ValidationError

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.core.database import get_current_db
from src.documents.models import Document
from src.core.auth.schemas import TokenPayload

from src.core.security import reusable_oauth2
from src.core.security import decode_token

from src.users.models import User
from src.users.models import Session


async def get_users_docs(
        user_id: int,
        db_session: AsyncSession
) -> List[Document]:
    result = await db_session.execute(
                select(Document).filter(Document.user_id == user_id)
            )
    logger.debug(f"User's documents: {result}")
    return result.scalars().all()


async def get_current_user(
    db_session: AsyncSession = Depends(get_current_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    """
    Method for get current user.

    :param db_session:
    :param token:
    """
    user_session = await Session.get_by_token(
        db_session=db_session,
        token=token
    )

    if not user_session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token is expired"
        )

    if user_session.expired:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Session is expired"
        )

    current_time = int(time.time())

    if user_session.expired_on < current_time:
        await user_session.set_expired(db_session=db_session)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token is expired"
        )

    if (current_time - user_session.updated_on) > 60:
        await user_session.time_update(
            db_session=db_session,
            new_time=current_time
        )

    try:
        payload = decode_token(str(user_session.token))
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        await user_session.set_expired(db_session=db_session)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token is expired"
        )
    except jwt.PyJWTError:
        await user_session.set_expired(db_session=db_session)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    except ValidationError:
        await user_session.set_expired(db_session=db_session)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = await User.get_by_id(
        db_session=db_session,
        id=token_data.sub
    )

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
