from hashlib import sha1
from .constants import RING_SIZE, BOOTSTRAP_NODE
import requests

def compute_sha1_hash(string):
    return int.from_bytes(sha1(string.encode()).digest(), byteorder='big') 

def compute_predecessor(candidates, node_hash):
    min_distance = float("inf")
    for candidate in candidates:
        candidate_hash = compute_sha1_hash(candidate)
        if candidate_hash < node_hash and node_hash - candidate_hash < min_distance:
            min_distance = node_hash - candidate_hash
            predecessor = candidate
        elif RING_SIZE - (candidate_hash - node_hash) < min_distance:
            min_distance = RING_SIZE - (candidate_hash - node_hash)
            predecessor = candidate
    return predecessor

def compute_successor(candidates, node_hash):
    min_distance = float("inf")
    for candidate in candidates:
        candidate_hash = compute_sha1_hash(candidate)
        if node_hash < candidate_hash and candidate_hash - node_hash < min_distance:
            min_distance = candidate_hash - node_hash
            successor = candidate
        elif RING_SIZE - (node_hash - candidate_hash) < min_distance:
            min_distance = RING_SIZE - (node_hash - candidate_hash)
            successor = candidate
    return successor

def bootstrap_has_joined():
    url = "http://" + BOOTSTRAP_NODE + "/bootstrap/management"
    contact_bootstrap = requests.get(url)
    bootstrap_joined = contact_bootstrap.json().get("result")

    if bootstrap_joined:
        return True
    return False


def check_responsible_set(hashed_key, node_hash, pred_hash):
    print(hashed_key)
    print(node_hash)
    print(pred_hash)
    if node_hash > pred_hash and \
            (hashed_key <= node_hash and hashed_key > pred_hash):
        print("case1")
        return True
    elif node_hash < pred_hash and \
            ((hashed_key > 0 and hashed_key <= node_hash) or hashed_key > pred_hash):
        print("case2")
        return True
    # Corner case: Only the bootstrap node is in the ring.
    elif node_hash == pred_hash:
        print("corner")
        return True
    return False

def accumulate_node_data(node_hash, raw_data):
    accumulator = {}
    node_data = {}
    for record in raw_data:
        accumulator[record.hashed_key] = (record.key, record.value)
    node_data[str(node_hash)] = accumulator
    return node_data
