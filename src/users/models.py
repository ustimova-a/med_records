import datetime
from typing import List

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.models.model_crud import BaseCRUD


class User(BaseCRUD):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    email: str = Column(String(255), nullable=False)
    login: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)  # hash
    superuser: bool = Column(Boolean, default=False)
    deleted: bool = Column(Boolean, default=False)

    documents = relationship(
        'Document', back_populates='user'
    )
    side_effects = relationship(
        'SideEffect', back_populates='user'
    )
