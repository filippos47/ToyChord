from models import KeyValuePair
from database import db

def create_or_update_entry(node_hash, key, value, hashed_key, replica_id):
    entry = KeyValuePair.query.filter_by(key = key).first()
    # Check if there is a pre-existing entry for the key
    if entry is None:
        entry = KeyValuePair(chordnode_id = str(node_hash),
                             key = key,
                             value = value,
                             hashed_key = str(hashed_key),
                             replica_id = replica_id)
        action = "Inserted "
        db.session.add(entry)
    else:
        entry.value = value
        action = "Updated "

    db.session.commit()
    response = action + "key-value pair {}:{}.".format(key, value)
    return response
