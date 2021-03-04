from flask import Response, request
from flask_restful import Resource

class Join(Resource):
    def post(self):
        source_ip = request.environ['REMOTE_ADDR']
        source_port = str(request.environ['REMOTE_PORT'])
        source_ip_port = source_ip + ":" + source_port
        return Response(source_ip_port, status=200)
