from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db
from models import KeyValuePair, ChordNode
from utils.common import compute_sha1_hash

class UpdatePredecessor(Resource):
    def post(self, new_predecessor):
        server_ip_port = request.host
        server_id = str(compute_sha1_hash(server_ip_port))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()
        new_predecessor_hash = compute_sha1_hash(new_predecessor)
       
        # Collect data that don't belong to me any more, deleting them from my
        # storage
        offloaded_data = {}
        storage = KeyValuePair.query.all()
        for entry in storage:
            if int(entry.hashed_key) < new_predecessor_hash:
                offloaded_data[entry.key] = entry.value
                db.session.delete(entry)
        print(offloaded_data)

        # Adjust my predecessor field
        my_identity.predecessor = new_predecessor
        db.session.commit()
        return offloaded_data

    def delete(self, new_predecessor):
        server_ip_port = request.host
        server_id = str(compute_sha1_hash(server_ip_port))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()

        incoming_data = request.json
        for key in incoming_data:
            data = KeyValuePair(chordnode_id = server_id,
                    key = key,
                    value = incoming_data[key],
                    hashed_key = str(compute_sha1_hash(key)))
            db.session.add(data)

        my_identity.predecessor = new_predecessor
        db.session.commit()
        return Response(status=200)
