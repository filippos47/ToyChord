from flask import Response
from flask_restful import Resource, Api
import requests
from flask import Flask, request
from utils.common import compute_sha1_hash, check_responsible_set
from models import ChordNode, KeyValuePair
from database import db


class Delete(Resource):
    def post(self):
        key = request.args.get('key')
        hashed_key = compute_sha1_hash(key)

        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None:
            pred_id = compute_sha1_hash(my_identity.predecessor)
            # If I am responsible for this key, I will delete it.
            if check_responsible_set(hashed_key, server_id, pred_id):
                record = KeyValuePair.query.filter_by(key = key).first()
                if record == None:
                    response, status =  "No such record exists.", 404
                else:
                    response, status =  "The key-value pair {}:{} is now deleted.".format(
                            key, record.value), 200
                    db.session.delete(record)
                    print(KeyValuePair.query.all())
                    db.session.commit()
            # Else, I will forward the request to my successor.
            else:
                url = "http://" + my_identity.successor + "/delete"
                response = requests.post(url, params = {'key': key})
                status = response.status_code

            return Response(response, status = status)
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
