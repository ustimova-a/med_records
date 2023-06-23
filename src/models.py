import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy_utils import URLType

from model_crud import BaseCRUD


class User(BaseCRUD):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    email: str = Column(String(255), nullable=False)
    password: str = Column(String(255), nullable=False)  # hash
    superuser: bool = Column(Boolean, default=False)
    deleted: bool = Column(Boolean, default=False)


class Hospital(BaseCRUD):
    __tablename__ = 'hospitals'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    website_url: str = Column(URLType(), nullable=True)  # str?
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)


class Specialty(BaseCRUD):
    __tablename__ = 'specialties'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Physician(BaseCRUD):
    __tablename__ = 'physicians'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    specialty_id: int = Column(Integer, ForeignKey("specialties.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    phone_number: int = Column(String(12), nullable=True)
    is_recommended: bool = Column(Boolean, default=False, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)


class Condition(BaseCRUD):
    __tablename__ = 'conditions'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Drug(BaseCRUD):
    __tablename__ = 'drugs'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Document(BaseCRUD):
    __tablename__ = 'documents'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    condition_id: int = Column(Integer, ForeignKey("conditions.id"))
    treatment_id: int = Column(Integer, ForeignKey("treatments.id"))
    source_doc_url: str = Column(URLType(), nullable=True)  # str?
    deleted: bool = Column(Boolean, default=False)


class Treatment(BaseCRUD):
    __tablename__ = 'treatments'

    id: int = Column(Integer, primary_key=True, index=True)
    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    dosage: float = Column(Float, nullable=True)
    per_day: int = Column(Integer, nullable=True)
    comment: str = Column(String(), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class Visit(BaseCRUD):
    __tablename__ = 'visits'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    document_id: int = Column(Integer, ForeignKey("documents.id"))
    comment: str = Column(String(), nullable=False)
    deleted: bool = Column(Boolean, default=False)


class SideEffect(BaseCRUD):
    __tablename__ = 'side_effects'

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    deleted: bool = Column(Boolean, default=False)
