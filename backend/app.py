from flask import Flask
from flask_restful import Api
from endpoints.routes import initialize_routes
from flask_migrate import Migrate
from database import db
from models import ChordNode, KeyValuePair, NodeRecord

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
initialize_routes(api)
