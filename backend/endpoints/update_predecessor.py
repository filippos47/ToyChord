from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db
from models import KeyValuePair, ChordNode
from utils.common import compute_sha1_hash

class UpdatePredecessor(Resource):
    def post(self, new_predecessor):
        source_ip_port = request.host
        hashed_id = str(compute_sha1_hash(source_ip_port))
        my_identity = ChordNode.query.filter_by(hashed_id = hashed_id).first()
        new_predecessor_hash = str(compute_sha1_hash(new_predecessor))
       
        # Collect data that don't belong to me any more, deleting them from my
        # storage
        offloaded_data = {}
        to_delete_data = KeyValuePair.query.filter(KeyValuePair.hashed_id <= new_predecessor_hash)
        for entry in to_delete_data:
            offloaded_data[entry.hashed_id] = entry.value
            db.session.delete(entry)

        # Adjust my predecessor field
        print(my_identity)
        my_identity.predecessor = new_predecessor
        print(my_identity)
        db.session.commit()
        return offloaded_data

    def delete(self, new_predecessor):
        source_ip_port = request.host
        hashed_id = str(compute_sha1_hash(source_ip_port))
        my_identity = ChordNode.query.filter_by(hashed_id = hashed_id).first()

        incoming_data = request.json
        for key in incoming_data:
            data = KeyValuePair(chordnode_id = hashed_id,
                    hashed_id = key,
                    value = delegated_data[key])
            db.session.add(data)

        my_identity.predecessor = new_predecessor
        db.session.commit()
        return Response(status=200)
