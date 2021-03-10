from flask import Response, request, jsonify
from flask_restful import Resource
import requests
from models import NodeRecord
from utils.common import compute_predecessor, compute_successor, compute_sha1_hash
from database import db

class Bootstrap(Resource):
    def post(self):
        new_node_ip = request.json['source_ip_port']

        nodes = []
        for node in NodeRecord.query.all():
            nodes.append(node.ip_port)
        new_node_hash = compute_sha1_hash(new_node_ip)
        new_node_predecessor = compute_predecessor(nodes, new_node_hash)
        new_node_successor = compute_successor(nodes, new_node_hash)

        if db.session.query(NodeRecord.id).filter_by(ip_port=new_node_ip).first() is None:
            new_node_record = NodeRecord(bootstrap_id = 1, ip_port = new_node_ip)
            db.session.add(new_node_record)
            db.session.commit()

        response = {'predecessor': new_node_predecessor, 
                'successor': new_node_successor}
        return response
