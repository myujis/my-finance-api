# for UUID ids

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql.functions import GenericFunction

class uuid_generate_v1mc(GenericFunction):
    type = UUID
