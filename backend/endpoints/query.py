from flask import Response
from flask_restful import Resource

class Query(Resource):
    def get(self, key):
        return Response(key, status=200)
