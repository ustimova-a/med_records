import datetime
from typing import Type
from typing import TypeVar
from typing import Union
from typing import Optional

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_token
from core.model_crud import BaseCRUD


# region User

T_USER = TypeVar('T_USER', bound='User')


class User(BaseCRUD):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    email: str = Column(String(255), nullable=False)
    login: str = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    superuser: bool = Column(Boolean, default=False)
    deleted: bool = Column(Boolean, default=False)

    documents = relationship(
        'Document', back_populates='user'
    )
    side_effects = relationship(
        'SideEffect', back_populates='user'
    )

    @classmethod
    async def get_user_by_login(
        cls: Type[T_USER],
        session: AsyncSession,
        login: str
    ) -> Union[T_USER, None]:
        user = (await session.execute(select(User)
                                      .where(User.login == login))).first()
        if user:
            return user[0]

        return None

# endregion


# region Session

T_SESSION = TypeVar('T_SESSION', bound='Session')


class Session(BaseCRUD):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String)
    created_on = Column(Integer)
    updated_on = Column(Integer)
    expired_on = Column(Integer)
    expired = Column(Boolean)
    user_agent = Column(String)

    @classmethod
    async def create(
        cls: Type[T_SESSION],
        db_session: AsyncSession,
        user: User,
        user_agent: Optional[str] = "Unknown"
    ) -> Union[T_SESSION, None]:
        """
        Method create session and return session model.

        :param cls:
        :param db_session:
        :param user:
        :param user_agent:
        :return:
        """
        expires_delta = datetime.timedelta(
            hours=10  # to config
        )
        expired_on = datetime.datetime.utcnow() + expires_delta
        token = create_token(subject=user.id, expires_delta=expires_delta)

        session = await cls.get_by_token(db_session=db_session, token=token)

        if session:
            return session

        session = cls(
            user_id=user.id,
            token=token,
            created_on=datetime.datetime.utcnow().timestamp(),
            updated_on=datetime.datetime.utcnow().timestamp(),
            expired_on=expired_on.timestamp(),
            expired=False,
            user_agent=user_agent
        )
        db_session.add(session)
        await db_session.commit()
        return await cls.get_by_token(db_session=db_session, token=token)

    async def set_expired(
            self,
            db_session: AsyncSession
    ) -> None:
        """
        Method set expired to user_sessions.

        :param db_session:
        """
        await db_session.execute(update(Session)
                                 .where(Session.id == self.id)
                                 .values(expired=True))
        await db_session.commit()
        self.expired = True

    async def time_update(
            self,
            db_session: AsyncSession,
            new_time: int
    ) -> None:
        """
        Method update time of session.

        :param db_session:
        :param new_time:
        """
        await db_session.execute(update(Session)
                                 .where(Session.id == self.id)
                                 .values(updated_on=new_time))
        self.updated_on = new_time

    @classmethod
    async def get_by_token(
        cls: Type[T_SESSION],
        db_session: AsyncSession,
        token: str
    ) -> Union[T_SESSION, None]:

        session = (await db_session.execute(select(Session)
                                            .where(Session.token == token))).first()
        if session:
            return session[0]
        return None

# endregion
