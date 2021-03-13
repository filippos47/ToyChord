from flask import Response
from flask_restful import Resource, Api
import requests
from flask import Flask, request
from utils.common import (
        compute_sha1_hash,
        check_responsible_set,
        handle_replicated_data,
)
from models import ChordNode, KeyValuePair
from database import db


class Delete(Resource):
    def post(self):
        key = request.args.get('key')
        server_id = compute_sha1_hash(request.host)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None and key is not None:
            hashed_key = compute_sha1_hash(key)
            pred_id = compute_sha1_hash(my_identity.predecessor)
            url = "http://" + my_identity.successor + "/delete"
            params = {'key': key}

            """
            When we receive a deletion request, there are two cases where we
            will have to handle it ourselves:
            1) If we are responsible for this key, we will delete it. Then,
               we must ensure that every other replica will be deleted, too. 
               In order to achieve this, we save in an HTTP header the 
               replica_id of our successor, and we forward the request to him.
            2) If we need to delete a replica of this entry, we will do so.
               As stated before, in this scenario the HTTP header `next_replica`
               will store the replica_id of our copy. Our predecessor is fully
               responsible for determining whether we hold a copy of an entry,
               or every replica has been deleted.
            """
            if check_responsible_set(hashed_key, server_id, pred_id) or \
                    request.args.get('next_replica') is not None:
                entry = KeyValuePair.query.filter_by(key = key).first()
                if entry is None:
                    response, status =  "No such record exists.", 404
                else:
                    try:
                        current_replica = int(request.args.get('next_replica'))
                    except:
                        current_replica = 1
                    response, status =  "The key-value pair {}:{} is now deleted.".format(
                            key, entry.value), 200
                    db.session.delete(entry)
                    db.session.commit()
                    handle_replicated_data(current_replica + 1, url, params)
            # Else, we just forward the deletion request until the responsible
            # node receives it.
            else:
                response = requests.post(url, params = params)
                status = response.status_code
            return Response(response, status = status)
        elif key is None:
            response = "You didn't specify a key!"
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
