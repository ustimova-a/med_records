from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from core.model_crud import BaseCRUD


class Condition(BaseCRUD):
    __tablename__ = 'conditions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    documents = relationship(
        'Document', back_populates='condition'
    )
