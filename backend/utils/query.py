def accumulate_node_data(node_hash, raw_data):
    accumulator = {}
    node_data = {}
    for entry in raw_data:
        accumulator[entry.hashed_key] = (entry.key, entry.value, entry.replica_id)
    node_data[str(node_hash)] = accumulator
    return node_data
