from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

# sqlite cheat to enable foreign key support
# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

db = SQLAlchemy()
