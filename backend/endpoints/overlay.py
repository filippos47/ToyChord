from flask import Response
from flask_restful import Resource

class Overlay(Resource):
    def get(self):
        return Response("Overlay", status=200)
