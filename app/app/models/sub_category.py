from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import FetchedValue

from sqlalchemy.orm import relationship, backref, deferred

from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, MONEY, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

from app.models.common import uuid_generate_v1mc


class SubCategory(Base):
    id = Column(UUID(as_uuid=True), server_default=uuid_generate_v1mc(), nullable=False, autoincrement=False,
                primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=False)
    category = relationship("Category", backref=backref('sub_categories'), order_by='SubCategory.row_created.asc()')

    name = Column(TEXT, unique=True, nullable=False)

    row_created = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified_user = Column(TEXT, server_default=FetchedValue(), server_onupdate=FetchedValue())

    def __init__(self, name=None,category_id=None):
        self.name = name
        self.category_id = category_id