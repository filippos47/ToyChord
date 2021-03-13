import requests
from .constants import BOOTSTRAP_NODE, REPLICATION_FACTOR

def bootstrap_has_joined():
    url = "http://" + BOOTSTRAP_NODE + "/bootstrap/management"
    contact_bootstrap = requests.get(url)
    bootstrap_joined = contact_bootstrap.json().get("result")
    if bootstrap_joined:
        return True
    return False

def fix_replication(key, successor):
    url = "http://" + successor + '/fix_replication/' + key
    requests.post(url)
