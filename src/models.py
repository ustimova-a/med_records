import datetime

from typing import TypeVar
from typing import Type
from typing import List

from sqlalchemy import select
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy_utils import URLType

from sqlalchemy.ext.asyncio import AsyncSession

from db import Base


T_BaseCRUD = TypeVar('T_BaseCRUD', bound='BaseCRUD')


class BaseCRUD(Base):
    __abstract__ = True
    id = Column(String, primary_key=True)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f")>"
        )

    @classmethod
    async def create(cls, **kwargs) -> Self:
        async with async_session() as db:
            server = cls(id=str(uuid4()), **kwargs)
            db.add(server)
            try:
                await db.commit()
                await db.refresh(server)
            except Exception:
                await db.rollback()
                raise
            return server

    @classmethod
    async def update(cls, id, **kwargs) -> Self:
        async with async_session() as db:
            query = (
                sqlalchemy_update(cls)
                .where(cls.id == id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(query)
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise
            return await cls.get(id)

    @classmethod
    async def get_by_id(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        result = await db_session.execute(
            select(cls).filter(cls.id == id and not cls.deleted)
        )
        return result.scalars().first()

    @classmethod
    async def get_all(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> List[T_BaseCRUD]:

        result = await db_session.execute(select(cls).filter(not cls.deleted))
        return result.scalars().all()

    @classmethod
    async def delete(cls, id) -> bool:
        async with async_session() as db:
            query = sqlalchemy_delete(cls).where(cls.id == id)
            await db.execute(query)
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise
            return True


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    superuser: bool = Column(Boolean, default=False)
    deleted: bool = Column(Boolean, default=False)


class Hospital(Base):
    __tablename__ = 'hospitals'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    website_url: str = Column(URLType(), nullable=True)  # str?
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)


class Specialty(Base):
    __tablename__ = 'specialties'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Physician(Base):
    __tablename__ = 'physicians'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    specialty_id: int = Column(Integer, ForeignKey("specialties.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    phone_number: int = Column(String(12), nullable=True)
    is_recommended: bool = Column(Boolean, default=False, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)


class Condition(Base):
    __tablename__ = 'conditions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Drug(Base):
    __tablename__ = 'drugs'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Document(Base):
    __tablename__ = 'documents'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    condition_id: int = Column(Integer, ForeignKey("conditions.id"))
    treatment_id: int = Column(Integer, ForeignKey("treatments.id"))
    source_doc_url: str = Column(URLType(), nullable=True)  # str?
    deleted: bool = Column(Boolean, default=False)


class Treatment(Base):
    __tablename__ = 'treatments'

    id: int = Column(Integer, primary_key=True, index=True)
    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    dosage: float = Column(Float, nullable=True)
    per_day: int = Column(Integer, nullable=True)
    comment: str = Column(String(), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Visit(Base):
    __tablename__ = 'visits'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    document_id: int = Column(Integer, ForeignKey("documents.id"))
    comment: str = Column(String(), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class SideEffect(Base):
    __tablename__ = 'side_effects'

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    deleted: bool = Column(Boolean, default=False)
