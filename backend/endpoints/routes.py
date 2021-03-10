from .insert import Insert
from .query import Query
from .delete import Delete
from .join import Join
from .depart import Depart
from .overlay import Overlay
from .bootstrap import Bootstrap
from .update_predecessor import UpdatePredecessor
from .update_successor import UpdateSuccessor

def initialize_routes(api):
    api.add_resource(Insert, '/insert/<string:key>/<string:value>')
    api.add_resource(Query, '/query/<string:key>')
    api.add_resource(Delete, '/delete/<string:key>')
    api.add_resource(Join, '/join')
    api.add_resource(Depart, '/depart')
    api.add_resource(Overlay, '/overlay')
    api.add_resource(Bootstrap, '/bootstrap/join')
    api.add_resource(UpdatePredecessor, '/update_predecessor/<string:new_predecessor>')
    api.add_resource(UpdateSuccessor, '/update_successor/<string:new_successor>')
