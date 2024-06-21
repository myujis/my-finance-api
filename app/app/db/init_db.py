from sqlalchemy.orm import Session

from app.core.config import settings

# next line does not quite work?
# from app.db import base
from app.db.base import *

from app.db.session import engine

from sqlalchemy import event


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28



# modified trigger
modified_trigger = """
    DROP TRIGGER IF EXISTS row_mod_on_{table_name}_trigger ON \"{table_name}\";
    CREATE TRIGGER row_mod_on_{table_name}_trigger
    BEFORE INSERT OR UPDATE
    ON \"{table_name}\"
    FOR EACH ROW
    EXECUTE PROCEDURE update_row_modified_function();
"""

def create_modified_trigger(target, connection, **kwargs):

    """
    This is used to add bookkeeping triggers after a table is created. It hooks
    into the SQLAlchemy event system. It expects the target to be an instance of
    MetaData.
    """
    for key in target.tables:
        table = target.tables[key]
        connection.execute(modified_trigger.format(table_name=table.name))

def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, set
    # USE_ALEMBIC in settings to False

    if not settings.USE_ALEMBIC:
        # hook triggers into db
        event.listen(Base.metadata, 'after_create', create_modified_trigger)
        # for uuid ids
        db.execute(""" CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\" """)
        # set datestyle to YYYY-MM-DD
        db.execute(""" SET DateStyle='ISO, YMD' """)
        # row modified function
        db.execute("""
            CREATE OR REPLACE FUNCTION update_row_modified_function()
            RETURNS TRIGGER AS
            $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    NEW.row_created = current_timestamp;
                    NEW.row_modified = current_timestamp;
                    NEW.row_modified_user = current_user;
                    RETURN NEW;
                ELSIF TG_OP = 'UPDATE' THEN
                    IF row(NEW.*) IS DISTINCT FROM row(OLD.*) THEN
                        NEW.row_created = OLD.row_created;
                        NEW.row_modified = current_timestamp;
                        NEW.row_modified_user = current_user;
                        RETURN NEW;
                    ELSE
                        RETURN OLD;
                    END IF;
                END IF;
            END;
            $$ LANGUAGE 'plpgsql';
        """)
        # we need to commit the functions before the next steps
        db.commit()

        Base.metadata.create_all(bind=engine)
