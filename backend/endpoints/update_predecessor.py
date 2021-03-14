from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db
from models import KeyValuePair, ChordNode
from utils.common import compute_sha1_hash

class UpdatePredecessor(Resource):
    def post(self, new_predecessor):
        server_id = str(compute_sha1_hash(request.host))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()
        new_predecessor_hash = compute_sha1_hash(new_predecessor)
       
        # Collect data that should be delegated to my new predecessor.
        delegated_data = {}
        storage = KeyValuePair.query.all()
        for entry in storage:
            if int(entry.hashed_key) < new_predecessor_hash:
                delegated_data[entry.key] = (entry.value, entry.replica_id)

        # Adjust my predecessor field
        my_identity.predecessor = new_predecessor
        db.session.commit()
        return delegated_data

    def delete(self, new_predecessor):
        server_id = str(compute_sha1_hash(request.host))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()
        # Adjust my predecessor field
        my_identity.predecessor = new_predecessor
        db.session.commit()
        return Response(status=200)
