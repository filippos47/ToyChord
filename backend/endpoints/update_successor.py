from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db

class UpdateSuccessor(Resource):
    def post(self, new_successor):
        # My db contains only myself, so this is fine.
        my_identity = ChordNode.query.get(1)
        my_identity.successor = new_successor
        db.session.commit()

        return Response(status = 200)
