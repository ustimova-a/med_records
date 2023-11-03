from typing import List
from typing import Type
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import logger
from core.database import Base


T_BaseCRUD = TypeVar('T_BaseCRUD', bound='BaseCRUD')


class BaseCRUD(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @classmethod
    async def create(
        cls: Type[T_BaseCRUD],
        cls_in,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        try:
            if 'date' in cls_in.__dict__ and cls_in.__dict__['date']:
                cls_in.__dict__['date'] = cls_in.__dict__['date'].replace(tzinfo=None)
            item = cls(**cls_in.__dict__)
            db_session.add(item)
            await db_session.commit()
            logger.debug(f'Item created: {item}')

        except Exception as e:
            await db_session.rollback()
            logger.error(e)

        return item

    @classmethod
    async def update(
        cls: Type[T_BaseCRUD],
        id: int,
        cls_in,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        try:
            if 'date' in cls_in.__dict__ and cls_in.__dict__['date']:
                cls_in.__dict__['date'] = cls_in.__dict__['date'].replace(tzinfo=None)

            query = (
                    update(cls)
                    .where(cls.id == id)
                    .values(**cls_in.__dict__)
                    # .execution_options(synchronize_session="fetch")
                )
            await db_session.execute(query)
            await db_session.commit()
            logger.debug(f'Item updated: {cls}')

        except Exception as e:
            await db_session.rollback()
            logger.error(e)

        return await cls.get_by_id(
            db_session=db_session,
            id=id
        )

    @classmethod
    async def get_by_id(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        try:
            result = await db_session.execute(
                select(cls).filter(cls.id == id)
            )
            logger.debug(f'Item provided: {result}')
        except Exception as e:
            logger.error(e)

        return result.scalars().first()

    @classmethod
    async def get_all(
        cls: Type[T_BaseCRUD],
        db_session: AsyncSession
    ) -> List[T_BaseCRUD]:

        result = await db_session.execute(select(cls))
        logger.debug(f'All items: {result}')
        return result.scalars().all()

    @classmethod
    async def delete(
        cls: Type[T_BaseCRUD],
        id: int,
        db_session: AsyncSession
    ) -> T_BaseCRUD:

        try:
            item = await cls.get_by_id(
                db_session=db_session,
                id=id
            )
            item.deleted = True
            await db_session.commit()
            logger.debug(f'Item deleted: {item}')

        except Exception as e:
            await db_session.rollback()
            logger.error(e)
