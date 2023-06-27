from typing import AsyncGenerator
from starlette.requests import Request
from pydantic.networks import PostgresDsn

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

import src.config as config


Base = declarative_base()


DATABASE_URI = PostgresDsn.build(
    scheme='postgresql+asyncpg',
    user=config.DATABASE_LOGIN,
    password=config.DATABASE_PASSWORD,
    host=config.DATABASE_HOST,
    port=config.DATABASE_PORT,
    path=f"/{config.DATABASE_NAME}"
)

async_engine = create_async_engine(
    DATABASE_URI,

    pool_size=config.DATABASE_POOL_SIZE,  # Размер пула сессий с базой данных. Кол-во
                                          # сессий будет всегда находится в памяти для
                                          # ускорения работы с базой.
                                          # -/ n.kushnarenko 22.10.2020

    max_overflow=config.DATABASE_POOL_MAX,  # Максимальный размер пула сессий с базой
                                            # данных. При нехватке кол-ва сессий, будут
                                            # создаваться дополнительные сессии и после
                                            # выполнения работы закрываться и удаляться
                                            # -/ n.kushnarenko 22.10.2020

    pool_pre_ping=True,  # Тестируем соединение при запросе. Иначе если соединение будет
                         # прервано администратором, первый запрос уйдёт с ошибкой
                         # -/ n.kushnarenko 22.10.2020

    connect_args={
        'server_settings': {
            'application_name': config.DATABASE_APPLICATION_NAME,  # Имя приложения которое отображается в таблице сессий базы данных.
        },

    },

    echo=False
)

SessionLocal = sessionmaker(
    async_engine, autoflush=False, class_=AsyncSession
)


async def get_current_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    yield request.state.db

    #     async with SessionLocal() as session:
    #         yield session
