import uvicorn
import asyncio

from core.database import Base
from core.database import async_engine
from core.logger import logger

# region model import
from conditions.models import *
from documents.models import *
from drugs.models import *
from hospitals.models import *
from physicians.models import *
from side_effects.models import *
from specialties.models import *
from treatments.models import *
from users.models import *
from visits.models import *
# endregion


async def create_db_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info('DB metadata created')


if __name__ == "__main__":
    #asyncio.run(create_db_tables())
    server_config = uvicorn.Config("core.app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
