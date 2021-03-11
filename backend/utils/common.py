from hashlib import sha1
from .constants import RING_SIZE, BOOTSTRAP_NODE
from models import NodeRecord

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
    if NodeRecord.query.filter_by(ip_port = BOOTSTRAP_NODE).first() != None:
        return True
    return False
