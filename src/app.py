import secrets
import uvicorn
from typing import List, Optional

from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import src.models as models
import schemas

app = FastAPI()

security = HTTPBasic()


def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security)
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"user"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"password"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


router = APIRouter(dependencies=[Depends(get_current_username)])


@router.get("/")
def login(username: str = Depends(get_current_username)):
    return {"username": username}


@router.get("/groups/", response_model=List[schemas.Group])
def get_group_list() -> List[models.Group]:
    return groups


@router.get("/groups/{id_group}/", response_model=List[schemas.Group])
def get_group_by_id(id_group: int) -> models.Group:
    result = [group for group in groups if group.id == id_group]
    return result


@router.post("/groups/{id_group}/", response_model=schemas.Group)
def create_group(id: int, name: str) -> models.Group:
    result = models.Group(id=id, name=name)
    groups.append(result)
    return result


@router.get("/items/", response_model=List[schemas.Item])
def get_item_list() -> List[models.Item]:
    return items


@router.get("/items/{id_item}/", response_model=List[schemas.Item])
def get_item_by_id(id_item: int) -> models.Item:
    result = [item for item in items if item.id == id_item]
    return result


@router.post("/items/{id_item}/", response_model=schemas.Item)
def create_item(
    id: int,
    name: str,
    id_group: int,
    description: Optional[str]
) -> models.Item:

    result = models.Item(
                         id=id, name=name,
                         id_group=id_group,
                         description=description
    )
    items.append(result)
    return result


@router.get("/groups/{id_group}/items/", response_model=List[schemas.Item])
def get_items_by_group(id_group: int) -> List[models.Item]:
    result = [item for item in items if item.id_group == id_group]
    return result


app.include_router(router)


if __name__ == "__main__":
    config = uvicorn.Config("views:app", port=8000)
    server = uvicorn.Server(config)
    server.run()
