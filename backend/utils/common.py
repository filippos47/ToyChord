from hashlib import sha1
import requests
import threading
import time
from .constants import REPLICATION_FACTOR, CONSISTENCY_MODE

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

# Cheat way to simulate non-blocking HTTP requests
# https://stackoverflow.com/questions/57637654/how-to-fire-and-forgot-a-http-request
def non_blocking_http_request(url, params):
    requests.post(url, params = params)

def handle_replicated_data(next_replica, url, params):
    if next_replica <= REPLICATION_FACTOR:
        """
        Use cases:
        1) During key deletion, not every replica has been deleted.
        2) During key insertion, not every replica has been created
        In both cases, forward the request to our successor.
        """
        params['next_replica'] = next_replica
        # requests library is blocking; this means that the user will
        # receive his response only AFTER every node has deleted/created his
        # replica.
        if CONSISTENCY_MODE == "CHAIN_REPLICATION":
            response = requests.post(url, params = params)
        # In this case, we want the user to receive a response immediately after
        # the MASTER replica is deleted/created. In order to achieve this, we
        # "improvise" :p
        else:
            t = threading.Thread(target=non_blocking_http_request,
                    args=[url, params])
            t.daemon = True
            t.start()


def fix_replication(key, successor, value = None):
    url = "http://" + successor + '/fix_replication/' + key
    # In this case, a node has departed and we are creating a new replica.
    if value is not None:
        params = {'value': value}
        requests.delete(url, params = params)
    # Here, a node has joined and we have to destroy a redundant replica.
    else:
        requests.post(url)
