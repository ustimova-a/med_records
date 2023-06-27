import uvicorn

from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Depends

import src.config as config
import src.models as models
import src.schemas as schemas
import src.service as service
import src.security as security

app = FastAPI()
router = APIRouter(dependencies=[Depends(security.get_current_username)])


@router.get("/")
def login(username: str = Depends(security.get_current_username)):
    return {"username": username}


# @router.get("/groups/", response_model=List[schemas.Group])
# def get_group_list() -> List[models.Group]:
#     return groups


app.include_router(router)


if __name__ == "__main__":
    server_config = uvicorn.Config("views:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
