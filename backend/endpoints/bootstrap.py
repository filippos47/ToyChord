from flask import Response, request, jsonify
from flask_restful import Resource
import requests
from models import NodeRecord
from utils.common import compute_sha1_hash
from utils.bootstrap import compute_predecessor, compute_successor
from database import db
 
class Bootstrap(Resource):
    # This endpoint verifies whether bootstrap node has joined the ring.
    def get(self):
        if NodeRecord.query.filter_by(ip_port = request.host).first() != None:
            return {"result": True}
        return {"result": False}

    # This endpoint registers a new node in the ring.
    def post(self):
        new_node_ip = request.json['source_ip_port']
        server_id = str(compute_sha1_hash(request.host))

        nodes = []
        for node in NodeRecord.query.all():
            nodes.append(node.ip_port)
        new_node_hash = compute_sha1_hash(new_node_ip)
        new_node_predecessor = compute_predecessor(nodes, new_node_hash)
        new_node_successor = compute_successor(nodes, new_node_hash)

        if NodeRecord.query.filter_by(ip_port=new_node_ip).first() is None:
            new_node_record = NodeRecord(bootstrap_id = server_id,
                    ip_port = new_node_ip)
            db.session.add(new_node_record)
            db.session.commit()

        response = {'predecessor': new_node_predecessor, 
                'successor': new_node_successor}
        return response

    # This endpoint unregisters a departing node from the ring.
    def delete(self):
        departing_node_ip = request.json['source_ip_port']

        departing_node_record = NodeRecord.query.filter_by(ip_port=departing_node_ip).first()
        db.session.delete(departing_node_record)
        db.session.commit()
        return Response(status=200)
