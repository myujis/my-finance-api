from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import FetchedValue
from typing import List

from sqlalchemy.orm import relationship, backref, deferred, validates, column_property

from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, MONEY, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

from app.models.common import uuid_generate_v1mc

class User(Base):
    id = Column(UUID(as_uuid=True), server_default=uuid_generate_v1mc(), nullable=False, autoincrement=False,
                primary_key=True)
    # transactions = relationship("Transactions", back_populates="user", uselist=True)
    # settings = relationship("Settings", back_populates="user", uselist=True)


    name = Column(TEXT)
    last_name = Column(TEXT)
    full_name = column_property(name + " " + last_name)
    email = Column(TEXT, unique=True)
    row_created = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified_user = Column(TEXT, server_default=FetchedValue(), server_onupdate=FetchedValue())


    def __init__(self, name=None, last_name=None,email=None):
        self.name = name
        self.last_name = last_name
        self.email = email