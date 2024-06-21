from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey
from sqlalchemy import FetchedValue

from sqlalchemy.orm import relationship, backref, deferred, validates

from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, MONEY, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

from app.models.common import uuid_generate_v1mc


class SettingsAssociation(Base):
    #IDS AND RELATIONSHIPS
    id = Column(UUID(as_uuid=True), server_default=uuid_generate_v1mc(), nullable=False, autoincrement=False,
                primary_key=True)
    
    settings_id = Column(UUID(as_uuid=True), ForeignKey("settings.id"), nullable=False)
    settings = relationship("Settings",backref=backref('settings_association', passive_deletes=all), order_by='SettingsAssociation.row_created.asc()')

    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id"), nullable=False)
    category = relationship("Category", backref=backref('settings_association', passive_deletes=all), order_by='SettingsAssociation.row_created.asc()')

    #DATA
    weight = Column(FLOAT, nullable=False)

    #HOUSEKEEPING
    row_created = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified_user = Column(TEXT, server_default=FetchedValue(), server_onupdate=FetchedValue())

    @validates('weight')
    def validate_weight(self, key, value):
        if not 0 < value <= 100:
            raise ValueError(f'Invalid percentage {key}: {value}')
        return value

    def __init__(self, weight=None, settings_id=None, category_id=None):
        self.weight = weight
        self.settings_id = settings_id
        self.category_id = category_id