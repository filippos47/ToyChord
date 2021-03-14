from flask import Response
from flask_restful import Resource, Api
from flask import Flask, request
from utils.common import (
        compute_sha1_hash,
        check_responsible_set,
        handle_replicated_data,
)
from utils.insert import create_or_update_entry
from models import ChordNode, KeyValuePair
import requests


class Insert(Resource):
    def post(self):
        key = request.args.get('key')
        value = request.args.get('value')
        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None and key is not None and value is not None:
            hashed_key = compute_sha1_hash(key)
            pred_id = compute_sha1_hash(my_identity.predecessor)
            url = "http://" + my_identity.successor + "/insert"
            params = {'key': key, 'value': value}
            """
            When we receive an insertion request, there are two cases where
            we will have to handle it ourselves:
            1) If we are responsible for this key, we will store it. Then,
               we will kickstart the replication process. In order to achieve
               this, we save in an HTTP header the replica_id our successor
               will have, and we forward the request to him.
            2) If we need to store a replica of this entry, we will do so.
               As stated before, in this scenario the HTTP header `next_replica`
               will store the replica_id that our copy will have. Our
               predecessor is fully responsible for determining whether we
               should store a copy of an entry, or the REPLICATION_FACTOR has
               already been reached.
            """
            if check_responsible_set(hashed_key, server_id, pred_id) or \
                    request.args.get('next_replica') is not None:
                try:
                    current_replica = int(request.args.get('next_replica'))
                except:
                    current_replica = 1
                response = create_or_update_entry(server_id, key, value,
                        hashed_key, current_replica)
                handle_replicated_data(current_replica + 1, url, params)
            # Else, we just forward the insertion request until the responsible
            # node receives it.
            else:
                response = requests.post(url, params = params)
            return Response(response, status = 200)
        elif key is None:
            response = "You didn't specify a key!"
        elif value is None:
            response = "You didn't specify a value!"
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
