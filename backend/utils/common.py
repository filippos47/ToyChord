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


def check_responsible_set(NodeID,predID,succID,hashed_key):
         case_1=hashed_key<=NodeID and hashed_key > predID
         case_2=False
         case_3=False
         case_4=False
         if  predID > NodeID :
            case_2=hashed_key>=0 and hashed_key<=NodeID
            case_3=hashed_key>=predID
         if predID==succID:
             case_4=True   
         return case_1 or case_2 or case_3 or case_4
