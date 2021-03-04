from flask import Response
from flask_restful import Resource, Api

class Insert(Resource):
    def post(self, key, value):
        response = key + " " + value
        return Response(response, status=200)
