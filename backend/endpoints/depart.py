from flask import Response
from flask_restful import Resource

class Depart(Resource):
    def post(self):
        return Response("Ciao", status=200)
