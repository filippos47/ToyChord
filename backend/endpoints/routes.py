from .insert import Insert
from .query import Query
from .delete import Delete
from .join import Join
from .depart import Depart
from .overlay import Overlay
from .bootstrap import Bootstrap
from .update_predecessor import UpdatePredecessor
from .update_successor import UpdateSuccessor
from .fix_replication import FixReplication

def initialize_routes(api):
    api.add_resource(Insert, '/insert')
    api.add_resource(Query, '/query')
    api.add_resource(Delete, '/delete')
    api.add_resource(Join, '/join')
    api.add_resource(Depart, '/depart')
    api.add_resource(Overlay, '/overlay')
    api.add_resource(Bootstrap, '/bootstrap/management')
    api.add_resource(UpdatePredecessor, '/update_predecessor/<string:new_predecessor>')
    api.add_resource(UpdateSuccessor, '/update_successor/<string:new_successor>')
    api.add_resource(FixReplication, '/fix_replication/<string:key>')
