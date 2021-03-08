from .insert import Insert
from .query import Query
from .delete import Delete
from .join import Join
from .depart import Depart
from .overlay import Overlay

def initialize_routes(api):
    api.add_resource(Insert, '/insert/<string:key>/<string:value>')
    api.add_resource(Query, '/query/<string:key>')
    api.add_resource(Delete, '/delete/<string:key>')
    api.add_resource(Join, '/join')
    api.add_resource(Depart, '/depart')
    api.add_resource(Overlay, '/overlay')
