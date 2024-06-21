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


class Settings(Base):
    id = Column(UUID(as_uuid=True), server_default=uuid_generate_v1mc(), nullable=False, autoincrement=False,
                primary_key=True)
    user_id = Column(UUID(as_uuid=True),ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref('settings', passive_deletes=all), order_by='Settings.row_created.asc()')

    
    # settings_association = relationship("SettingsAssociation", back_populates="settings", uselist=True)

    row_created = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified_user = Column(TEXT, server_default=FetchedValue(), server_onupdate=FetchedValue())

    def __init__(self, user_id=None):
        self.user_id = user_id