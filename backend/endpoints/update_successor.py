from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db
from utils.common import compute_sha1_hash

class UpdateSuccessor(Resource):
    def post(self, new_successor):
        hashed_id = str(compute_sha1_hash(request.host))
        my_identity = ChordNode.query.filter_by(hashed_id = hashed_id).first()
        my_identity.successor = new_successor
        db.session.commit()

        return Response(status = 200)
