from flask import Response
from flask_restful import Resource, Api
from flask import Flask, request
from utils.common import (
        compute_sha1_hash,
        check_responsible_set,
        accumulate_node_data,
)
from models import ChordNode, KeyValuePair
from database import db
import requests

class Query(Resource):
    def get(self):
        key=request.args.get('key')
        hashed_key=compute_sha1_hash(key)

        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None:
            pred_id=int(compute_sha1_hash(my_identity.predecessor))
            succ_id=int(compute_sha1_hash(my_identity.successor))

            # Normal Query
            if key != '*':
                # If I am responsible for this key, I will answer the query.
                if check_responsible_set(hashed_key, server_id, pred_id):
                    record = KeyValuePair.query.filter_by(key = key).first()
                    if record == None:
                        response, status =  "No such record exists.", 404
                    else:
                        response, status =  "The requested key-value pair is {}:{}".format(
                                key, record.value), 200
                # Else, I will forward the request to my successor.
                else:
                    url = "http://" + my_identity.successor + "/query"
                    response = requests.get(url, params = {'key': key})
                    status = response.status_code

                return Response(response, status = status)
            # Return all songs per node. To achieve this, we make a full circle of
            # the ring.
            else:
                # The initially queried node initializes a dictionary, in which each
                # node will append his key-value pairs. He also saves himself as the
                # starting id, so as to identify when the full circle is completed.
                if request.args.get('starting_id') == None:    
                    # By the time a response is received, every node will have
                    # appended its key-value storage to the dictionary we created.
                    # It's time we return this dictionary to the user.
                    node_data = accumulate_node_data(server_id,
                            KeyValuePair.query.all())
                    url = "http://" + my_identity.successor + "/query"
                    response = requests.get(url, params = {'key': key,
                        'starting_id': str(server_id)} , json = node_data)
                    
                    # Sort by key first!
                    storage = response.json()
                    sorted_storage = dict(sorted(storage.items(),
                        key = lambda kv: int(kv[0])))
                    return sorted_storage
                else:
                    # A full circle has been completed.
                    if request.args.get('starting_id') == str(server_id):
                        return request.json
                    # Append my key-value storage and forward the request to my
                    # successor.
                    else:
                        received_node_data = request.json
                        node_data = accumulate_node_data(server_id,
                                KeyValuePair.query.all())
                        merged_node_data = {**node_data, **received_node_data}

                        url = "http://" + my_identity.successor + "/query"
                        response = requests.get(url, params = {'key': key,
                            'starting_id': request.args.get('starting_id')},
                            json = merged_node_data)

                        return response.json()
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
