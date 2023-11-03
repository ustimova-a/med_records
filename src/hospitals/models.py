from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from core.model_crud import BaseCRUD


class Hospital(BaseCRUD):
    __tablename__ = 'hospitals'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    website_url: str = Column(String(), nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    physicians = relationship(
        'Physician', back_populates='hospital'
    )
    documents = relationship(
        'Document', back_populates='hospital'
    )
    visits = relationship(
        'Visit', back_populates='hospital'
    )
