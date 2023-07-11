import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.models.model_crud import BaseCRUD


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


class Specialty(BaseCRUD):
    __tablename__ = 'specialties'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    physicians = relationship(
        'Physician', back_populates='specialty'
    )


class Physician(BaseCRUD):
    __tablename__ = 'physicians'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    phone_number: int = Column(String(12), nullable=True)
    is_recommended: bool = Column(Boolean, default=False, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    specialty_id: int = Column(Integer, ForeignKey("specialties.id"))
    specialty = relationship(
        'Specialty', back_populates='physicians'
    )

    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship(
        'Hospital', back_populates='physicians'
    )

    documents = relationship(
        'Document', back_populates='physician'
    )
    visits = relationship(
        'Visit', back_populates='physician'
    )


class Condition(BaseCRUD):
    __tablename__ = 'conditions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    documents = relationship(
        'Document', back_populates='condition'
    )


class Drug(BaseCRUD):
    __tablename__ = 'drugs'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    treatment = relationship(
        'Treatment', back_populates='drug'
    )
    side_effects = relationship(
        'SideEffect', back_populates='drug'
    )


class Treatment(BaseCRUD):
    __tablename__ = 'treatments'

    id: int = Column(Integer, primary_key=True, index=True)
    dosage: float = Column(Float, nullable=True)
    per_day: int = Column(Integer, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    drug = relationship(
        'Drug', back_populates='treatment'
    )

    documents = relationship(
        'Document', back_populates='treatment'
    )


class Visit(BaseCRUD):
    __tablename__ = 'visits'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    physician = relationship(
        'Physician', back_populates='visits'
    )

    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship(
        'Hospital', back_populates='visits'
    )

    document_id: int = Column(Integer, ForeignKey("documents.id"))
    document = relationship(
        'Document', back_populates='visits'
    )


class SideEffect(BaseCRUD):
    __tablename__ = 'side_effects'

    id: int = Column(Integer, primary_key=True, index=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        'User', back_populates='side_effects'
    )

    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    drug = relationship(
        'Drug', back_populates='side_effects'
    )
