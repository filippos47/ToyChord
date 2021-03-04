from flask import Response
from flask_restful import Resource, Api

class Delete(Resource):
    def post(self, key):
        return Response(key, status=200)
