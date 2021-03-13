from hashlib import sha1
import requests
from .constants import REPLICATION_FACTOR

def compute_sha1_hash(string):
    return int.from_bytes(sha1(string.encode()).digest(), byteorder='big') 

def check_responsible_set(hashed_key, node_hash, pred_hash):
    if node_hash > pred_hash and \
            (hashed_key <= node_hash and hashed_key > pred_hash):
        return True
    elif node_hash < pred_hash and \
            ((hashed_key > 0 and hashed_key <= node_hash) or hashed_key > pred_hash):
        return True
    # Corner case: Only the bootstrap node is in the ring.
    elif node_hash == pred_hash:
        return True
    return False

def handle_replicated_data(next_replica, url, params, deleting_data = False):
    if next_replica <= REPLICATION_FACTOR:
        params['next_replica'] = next_replica
        # Not every replica has been deleted; forward the request to our
        # successor.
        if deleting_data:
            deletion_response = requests.post(url, params = params)
        # The replication target has not been achieved; forward the request to
        # our successor.
        else:
            replication_response = requests.post(url, params = params)

def fix_replication(key, successor, value = None):
    url = "http://" + successor + '/fix_replication/' + key
    # In this case, a node has departed and we are creating a new replica.
    if value is not None:
        params = {'value': value}
        requests.delete(url, params = params)
    # Here, a node has joined and we have to destroy a redundant replica.
    else:
        requests.post(url)
