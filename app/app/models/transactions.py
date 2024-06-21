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


class Transactions(Base):
    id = Column(UUID(as_uuid=True), server_default=uuid_generate_v1mc(), nullable=False, autoincrement=False,
                primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    user = relationship("User", backref=backref('transactions', passive_deletes=all), order_by='Transactions.row_created.asc()')

    sub_category_id = Column(UUID(as_uuid=True), ForeignKey('subcategory.id'), nullable=False)
    sub_category = relationship("SubCategory", backref=backref('transactions', passive_deletes=all), order_by='Transactions.row_created.asc()')

    value = Column(FLOAT)
    date = Column(DATE)
    transaction_type = Column(TEXT)
    flag_installment = Column(BOOLEAN)
    installment_quantity = Column(INTEGER)

    row_created = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified = Column(TIMESTAMP(timezone=True), server_default=FetchedValue(), server_onupdate=FetchedValue())
    row_modified_user = Column(TEXT, server_default=FetchedValue(), server_onupdate=FetchedValue())

    def __init__(self, user_id=None,sub_category_id=None,value=None,date=None,transaction_type=None,flag_installment=None,installment_quantity=None):
        self.user_id = user_id
        self.sub_category_id = sub_category_id
        self.value = value
        self.date = date
        self.transaction_type = transaction_type
        self.flag_installment = flag_installment
        self.installment_quantity = installment_quantity