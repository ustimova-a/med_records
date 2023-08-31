from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from core.model_crud import BaseCRUD


class SideEffect(BaseCRUD):
    __tablename__ = 'side_effects'

    id: int = Column(Integer, primary_key=True, index=True)
    comment: str = Column(String(), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        'User', back_populates='side_effects'
    )

    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    drug = relationship(
        'Drug', back_populates='side_effects'
    )
