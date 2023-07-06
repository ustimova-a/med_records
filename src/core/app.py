import uvicorn

from fastapi import FastAPI
from fastapi import APIRouter

import src.documents.service as doc_service

from src.core.views import router as core_router
from src.documents.views import router as doc_router
from src.users.views import router as user_router

from src.core.database import get_current_db


app = FastAPI()

app.add_route('/storage/{filename:path}', doc_service.get_file, ['GET'])


# region router

router = APIRouter()
app.include_router(router)

app.include_router(core_router)
app.include_router(doc_router)
app.include_router(user_router)

# endregion


if __name__ == "__main__":
    server_config = uvicorn.Config("app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
