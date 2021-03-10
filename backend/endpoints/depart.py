from flask import Response, request
from flask_restful import Resource
import requests
from database import db
from utils.constants import BOOTSTRAP_NODE
from utils.common import compute_sha1_hash
from models import ChordNode, KeyValuePair, NodeRecord

class Depart(Resource):
    def post(self):
        # Chord node ip:port = server's ip:port.
        source_ip_port = request.host
        hashed_id = str(compute_sha1_hash(source_ip_port))

        # Ensure that this Chord node has already joined the ring.
        if ChordNode.query.filter_by(hashed_id=hashed_id).first() is not None:
            if source_ip_port != BOOTSTRAP_NODE:
                my_identity = ChordNode.query.filter_by(hashed_id = hashed_id).first()
                successor = my_identity.successor
                predecessor = my_identity.predecessor

                # First, contact bootstrap node to get deleted
                url = "http://" + BOOTSTRAP_NODE + '/bootstrap/join'
                bootstrap_response = requests.delete(url,
                        json={'source_ip_port': source_ip_port})

                # Then, gather all stored data for handover.

                offloaded_data = {}
                to_delete_data = KeyValuePair.query.all()
                for entry in to_delete_data:
                    offloaded_data[entry.hashed_id] = entry.value
                    db.session.delete(entry)

                # Now, communicate with our successor to inform him that we are
                # leaving and hand over our data.

                url = "http://" + successor + '/update_predecessor/' + predecessor
                successor_response = requests.delete(url, json = offloaded_data)

                # Also, communicate with our predecessor to inform him that we are
                # leaving.

                url = "http://" + predecessor + '/update_successor/' + successor
                predecessor_response = requests.post(url)

                # Finally, delete our identity from the db.
                db.session.delete(my_identity)
                db.session.commit()
                response = "Node left, with hashed id:{}".format(hashed_id)
            else:
                response = "You are the bootstrap node, you cannot leave!!!"
        else:
            response = "You are not in the ring yet!"

        print(ChordNode.query.all())
        return Response(response, status=200)
