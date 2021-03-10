from flask import Response, request
from flask_restful import Resource
from models import ChordNode
from database import db
from models import KeyValuePair, ChordNode
from utils.common import compute_sha1_hash

class UpdatePredecessor(Resource):
    def post(self, new_predecessor):
        new_predecessor_hash = compute_sha1_hash(new_predecessor)
        # My db contains only myself, so this is fine.
        my_identity = ChordNode.query.get(1)
        cur_predecessor_hash = compute_sha1_hash(my_identity.predecessor)
       
        # Collect data that don't belong to me any more, deleting them from my
        # storage
        offloaded_data = {}
        to_delete_data = KeyValuePair.query.filter(KeyValuePair.hashed_id <= str(new_predecessor_hash))
        for entry in to_delete_data:
            offloaded_data[str(entry.hashed_id)] =  entry.value
            db.session.delete(entry)

        # adjust my predecessor field
        my_identity.predecessor = new_predecessor
        db.session.commit()

        return offloaded_data
