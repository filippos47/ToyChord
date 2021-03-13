from flask import Response
from flask_restful import Resource, Api
from flask import Flask,request
from utils.common import compute_sha1_hash,check_responsible_set
from models import ChordNode,KeyValuePair
from database import db
import requests


class Insert(Resource):
    def post(self):
        key = request.args.get('key')
        value = request.args.get('value')
        hashed_key = compute_sha1_hash(key)

        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None:
            pred_id = compute_sha1_hash(my_identity.predecessor)
            # If I am responsible for this key, I will store it.
            if check_responsible_set(hashed_key, server_id, pred_id):
                record = KeyValuePair.query.filter_by(key = key).first()
                # Check if I already have a record for the key
                if record == None:
                    record = KeyValuePair(chordnode_id = str(server_id),
                            key = key,
                            value = value,
                            hashed_key = str(hashed_key))
                    db.session.add(record)
                    print(KeyValuePair.query.all())
                    db.session.commit()
                    
                    response = "Inserted key-value pair {}:{}, at node with id {}".format(
                            key, value, server_id)
                # If not, create it.
                else:
                    record = KeyValuePair.query.filter_by(key = key).first()
                    record.value = value
                    print(KeyValuePair.query.all())
                    db.session.commit()

                    response = "Updated key-value pair {}:{}, at node with id {}".format(
                            key, value, server_id)
            # Else, I will forward the request to my successor.
            else:
                url = "http://" + my_identity.successor + "/insert"
                response = requests.post(url,
                        params = {'key': key,'value': value})

            return Response(response, status = 200)
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
