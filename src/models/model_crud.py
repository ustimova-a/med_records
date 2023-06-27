from typing import List
from typing import Type
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.encoders import jsonable_encoder

from src.database import Base


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
    async def create(
        cls: Type[T_BaseCRUD],
        cls_in,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        item = await cls.get_by_id(
            db_session=db_session,
            id=cls_in.id
        )

        if item is None:
            item = cls(**cls_in.__dict__)  # ?
            db_session.add(item)

        if item.deleted:
            item.deleted = False

        try:
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            print(e)  # logger

        return item

    @classmethod
    async def update(
        cls: Type[T_BaseCRUD],
        cls_in,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        query = (
                update(cls)
                .where(cls.id == cls_in.id)
                .values(**cls_in.__dict__)
                # .execution_options(synchronize_session="fetch")
            )
        await db_session.execute(query)

        # item = await cls.get_by_id(
        #     db_session=db_session,
        #     id=cls_in.id
        # )
        # prev_data = jsonable_encoder(item)

        # if isinstance(cls_in, dict):
        #     update_data = cls_in
        # else:
        #     update_data = cls_in.dict(exclude_unset=True)

        # for field in prev_data:
        #     if field in update_data:
        #         setattr(item, field, update_data[field])

        try:
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            print(e)  # logger

        return await cls.get_by_id(
            db_session=db_session,
            id=cls_in.id
        )  # item

    @classmethod
    async def get_by_id(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        result = await db_session.execute(
            select(cls).filter(cls.id == id)
        )
        return result.scalars().first()

    @classmethod
    async def get_all(
        cls: Type[T_BaseCRUD],
        db_session: AsyncSession
    ) -> List[T_BaseCRUD]:

        result = await db_session.execute(select(cls))
        return result.scalars().all()

    @classmethod
    async def delete(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        item = await db_session.execute(
            select(cls).filter(cls.id == id)
        )
        item.deleted = True

        try:
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            print(e)  # logger

        return item.scalars().first()
