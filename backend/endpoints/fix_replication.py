from flask import Response, request
from flask_restful import Resource
import requests
from database import db
from utils.constants import REPLICATION_FACTOR
from utils.common import compute_sha1_hash
from models import KeyValuePair, ChordNode

class FixReplication(Resource):
    # This method is called when a new node has been inserted.
    def post(self, key):
        server_id = str(compute_sha1_hash(request.host))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()

        entry = KeyValuePair.query.filter_by(key = key).first()
        if entry.replica_id == REPLICATION_FACTOR:
            db.session.delete(entry)
        else:
            entry.replica_id += 1
            url = "http://" + my_identity.successor + "/fix_replication/" + key
            response = requests.post(url)

        db.session.commit()
        return Response(status = 200)
    # This method is called when a node has departed.
    def delete(self, key):
        server_id = str(compute_sha1_hash(request.host))
        my_identity = ChordNode.query.filter_by(hashed_id = server_id).first()

        value = request.args.get('value')
        entry = KeyValuePair.query.filter_by(key = key).first()
        if entry is None:
            entry = KeyValuePair(chordnode_id = server_id,
                                 key = key,
                                 value = value,
                                 hashed_key = str(compute_sha1_hash(key)),
                                 replica_id = REPLICATION_FACTOR)
            db.session.add(entry)
        else:
            entry.replica_id -= 1
            url = "http://" + my_identity.successor + "/fix_replication/" + key
            params = {'value': value}
            response = requests.delete(url, params = params)

        db.session.commit()
        return Response(status = 200)
