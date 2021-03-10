from database import db

class ChordNode(db.Model):
    __tablename__ = 'chordnode'

    id = db.Column(db.Integer, primary_key=True)
    hashed_id = db.Column(db.String)
    successor = db.Column(db.String)
    predecessor = db.Column(db.String)
    is_bootstrap = db.Column(db.Boolean, default=False)
    storage = db.relationship("KeyValuePair")
    node_map = db.relationship("NodeRecord", cascade="delete")

    def __repr__(self):
        return 'Chord node {}, with successor: {}, predecessor: {}, ' \
               'bootstrap: {}'.format(self.hashed_id, self.successor,
                self.predecessor, self.is_bootstrap)

class KeyValuePair(db.Model):
    __tablename__ = 'keyvaluepair'

    id = db.Column(db.Integer, primary_key=True)
    chordnode_id = db.Column(db.String, db.ForeignKey('chordnode.id'), nullable=True)
    hashed_id = db.Column(db.String)
    value = db.Column(db.String)

    def __repr__(self):
        return  '<key-value pair: {}:{}, responsible Chord node: {}'.format(self.hashed_id,
                self.value, self.chordnode_id)

class NodeRecord(db.Model):
    __tablename__ = 'noderecord'

    id = db.Column(db.Integer, primary_key=True)
    bootstrap_id = db.Column(db.Integer, db.ForeignKey('chordnode.id'), nullable=False)
    ip_port = db.Column(db.String)

    def __repr__(self):
        return 'Node record {} on bootstrap node with id {}'.format(self.ip_port,
                self.bootstrap_id)
