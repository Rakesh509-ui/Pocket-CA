from __future__ import annotations

import json
from contextlib import contextmanager
from functools import lru_cache
from threading import Lock
from typing import Iterator
from uuid import uuid4

from sqlalchemy import (Boolean,Float,ForeignKey,Integer,String,Text,create_engine,select)
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import (DeclarativeBase,Mapped,Session,mapped_column,relationship,sessionmaker)
from sqlalchemy.types import JSON

from PocketCA.config import (
    DATABASE_URL,
    LEGACY_CHAT_SESSION_STORE_PATH,
    LEGACY_CHUNK_CATALOG_PATH,
    LEGACY_INGESTION_MANIFEST_PATH,
    LEGACY_USER_PROFILE_STORE_PATH,
    STORAGE_DIR,
)

from PocketCA.models import (ChatSession,ChatTurn,ChunkCatalogRecord,UserTaxProfile)

class Base(DeclarativeBase):
    pass

class UserProfileRow(Base):
    _tablename_ = "user_profiles"

    user_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(255),nullable=True,)
    profession_type: Mapped[str] = mapped_column(String(32),nullable=False,default="unknown",)
    tax_regime: Mapped[str] = mapped_column(String(32),nullable=False,default="unknown",)
    financial_year: Mapped[str] = mapped_column(String(32),nullable=False,)
    assessment_year: Mapped[str] = mapped_column(String(32),nullable=False,)
    age: Mapped[int | None] = mapped_column(Integer,nullable=True,)
    residential_status: Mapped[str] = mapped_column(String(64),nullable=False,)
    employer_type: Mapped[str] = mapped_column(String(64),nullable=False,)

    salary_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    pension_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    freelance_receipts: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    freelance_expenses: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    business_receipts: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    business_expenses: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    interest_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,) 
    savings_interest_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    fixed_deposit_interest_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    rental_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    other_income: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    capital_gains_special_rate: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)

    use_presumptive_profession: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False,)
    presumptive_profession_rate: Mapped[float] = mapped_column(Float,nullable=False,default=0.5,)
    use_presumptive_business: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False,)
    presumptive_business_rate: Mapped[float] = mapped_column(Float,nullable=False,default=0.08,)

    salary_standard_deduction_enabled: Mapped[bool] = mapped_column(Boolean,nullable=False,default=True,)
    exempt_allowances_old_regime: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    house_property_interest_self_occupied: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    employer_nps_contribution: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80c_total: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80ccd1b: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80d_self_family: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80d_parents: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80ee_interest: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80g_donations: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)
    section_80ccb_contribution: Mapped[float] = mapped_column(Float,nullable=False,default=0.0,)

    parents_are_senior_citizens: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False,)
    notes: Mapped[list[str]] = mapped_column(JSON,nullable=False,default=list,)
    known_facts: Mapped[list[str]] = mapped_column(JSON,nullable=False,default=list,)
    missing_fields: Mapped[list[str]] = mapped_column(JSON,nullable=False,default=list,)
    updated_at: Mapped[str] = mapped_column(String(64),nullable=False,)

class ChatSessionRow(Base):
    _tablename_ = "chat_sessions"

    session_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)

    turns: Mapped[list["ChatTurnRow"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatTurnRow.position",
    )

class ChatTurnRow(Base):
    _tablename_ = "chat_turns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(255),
        ForeignKey("chat_sessions.session_id",ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    position: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

    session: Mapped[ChatSessionRow] = relationship(back_populates="turns")

class ChunkCatalogRow(Base):
    _tablename_ = "chunk_catalog"

    chunk_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    document_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    page_number: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    section_title: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    statute_reference: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    chunk_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    document_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    document_year: Mapped[str | None] = mapped_column(String(32), nullable=True)


class IngestionRunRow(Base):
    __tablename__ = "ingestion_runs"

    run_id: Mapped[str] = mapped_column(String(32),primary_key=True,default=lambda: uuid4().hex,)
    backend: Mapped[str] = mapped_column(String(64), nullable=False)
    source_files: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    document_count: Mapped[int] = mapped_column(Integer, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_count: Mapped[int] = mapped_column(Integer, nullable=False)
    neo4j_database: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_backend: Mapped[str] = mapped_column(String(64), nullable=False, default="database")
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)

_PROFILE_FIELDS = tuple(UserTaxProfile.model_fields.keys())
_DATABASE_INIT_LOCK = Lock()
_DATABASE_INITIALIZED = False


def database_backend_name() -> str:
    return make_url(DATABASE_URL).get_backend_name()


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    connect_args: dict[str, object] = {}

