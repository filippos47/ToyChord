from flask import Response
from flask_restful import Resource, Api
from flask import Flask, request
from utils.common import compute_sha1_hash, check_responsible_set
from utils.query import accumulate_node_data
from utils.constants import REPLICATION_FACTOR, CONSISTENCY_MODE
from models import ChordNode, KeyValuePair
from sqlalchemy import and_
from database import db
import requests

class Query(Resource):
    def get(self):
        key=request.args.get('key')
        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None and key is not None:
            # Normal Query
            if key != '*':
                sql_query = KeyValuePair.query.filter(KeyValuePair.key == key)
                # If we want chain replication, only the last replica of the
                # queried entry should answer our query.
                if CONSISTENCY_MODE == "CHAIN_REPLICATION":
                    sql_query.filter(KeyValuePair.replica_id == REPLICATION_FACTOR)
                # Else, any replica can answer our query.
                entry = sql_query.first()
                if entry is not None:
                    response, status =  "The requested key-value pair is {}:{}".format(
                            key, entry.value), 200
                # Else, we will forward the request to our successor.
                else:
                    # The initially queried node sets an HTTP header, containing
                    # its IP. If we make a full circle without finding the last
                    # replica of the requested entry, we return 404.
                    starting_id = request.args.get('starting_id')
                    if starting_id != str(server_id):
                        if starting_id is None:
                            starting_id = str(server_id)
                        url = "http://" + my_identity.successor + "/query"
                        params = {'key': key, 'starting_id': starting_id}
                        response = requests.get(url, params = params)
                        status = response.status_code
                    else:
                        response, status =  "No such record exists.", 404

                return Response(response, status = status)
            # Return every entry per node. To achieve this, we make a full
            # circle of the ring.
            else:
                url = "http://" + my_identity.successor + "/query"
                # The initially queried node initializes a dictionary, in which each
                # node will append his key-value pairs. He also saves himself as the
                # starting id, so as to identify when the full circle is completed.
                if request.args.get('starting_id') is None:    
                    # By the time a response is received, every node will have
                    # appended its key-value storage to the dictionary we created.
                    # It's time we return this dictionary to the user.
                    node_data = accumulate_node_data(server_id,
                            KeyValuePair.query.all())
                    params = {'key': key, 'starting_id': str(server_id)}
                    response = requests.get(url, params = params, json = node_data)
                    
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

                        params = {'key': key, 'starting_id': request.args.get('starting_id')}
                        response = requests.get(url, params = params,
                            json = merged_node_data)

                        return response.json()
        elif key is None:
            response = "You didn't specify a key!"
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
