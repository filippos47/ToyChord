from flask import Flask
from flask_restful import Api
from endpoints.routes import initialize_routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.engine import Engine
from sqlalchemy import event

# sqlite cheat
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import ChordNode, KeyValuePair

api = Api(app)
initialize_routes(api)
