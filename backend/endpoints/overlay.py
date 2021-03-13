from flask import Response, request
from flask_restful import Resource
from models import ChordNode
import requests
from utils.common import compute_sha1_hash

class Overlay(Resource):
    def get(self):
        # Chord node ip:port = server's ip:port.
        server_ip_port = request.host
        server_id = compute_sha1_hash(server_ip_port)
        my_identity = ChordNode.query.filter_by(hashed_id = str(server_id)).first()

        if my_identity is not None:
            successor = my_identity.successor

            # `nodes_traversed` is a dictionary storing entries of the form
            # "server ip and port":"server hashed id".
            # Get nodes traversed until now..
            if request.json is not None:
                nodes_traversed = request.json
            # ..or initialize the dictionary if no node has been traversed yet.
            else:
                nodes_traversed = {}

            # Add ourselved to the traversed nodes.
            nodes_traversed[server_ip_port] = server_id

            # If my successor is already in the list, it means that a full circle
            # has been completed, and no more forwarding is needed.
            if successor in nodes_traversed:
                # Now, we will respond to our predecessor, inserting a counter in
                # the dictionary equal to the number of nodes in the ring (other
                # than us). Each node will decrement this counter by one. When this
                # counter is equal to zero, it means that we have returned to the
                # starting point, and can finally return the overlay topology to the
                # user.
                nodes_traversed["counter"] = len(nodes_traversed) - 1
                return nodes_traversed

            # Else, just forward the request (and the nodes_traversed dictionary)
            # to our successor, after adding ourselves in the dictionary.
            else:
                nodes_traversed[server_ip_port] = server_id
                url = "http://" + successor + "/overlay"
                forwarding_response = requests.get(url, json = nodes_traversed)
                overlay = forwarding_response.json()

                # When we finally receive a response from our successor, it means
                # that the circle was completed and we are going the other way
                # around, back to the starting point.
                # First, decrement the counter by one.
                overlay["counter"] -= 1

                # If counter is now equal to zero, we have got back to the starting
                # point. It's time to return the overlay topology to the user.
                if overlay["counter"] == 0:
                    del overlay["counter"]

                    # We have to return the topology in the correct orded. Now it's
                    # mixed-up. We will sort the overlay by the hashed ids.
                    sorted_overlay = {k: v for k, v in sorted(overlay.items(),
                        key=lambda item: item[1])}
                    return sorted_overlay
                # Else, just respond to our predecessor.
                else:
                    return overlay
        else:
            response = "You must be in the ring to perform operations!"
            return Response(response, status = 401)
