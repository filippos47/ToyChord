from app import db

class ChordNode(db.Model):
    __tablename__ = 'chordnode'

    id = db.Column(db.Integer, primary_key=True)
    hashed_id = db.Column(db.Integer)
    successor = db.Column(db.Integer)
    predecessor = db.Column(db.Integer)
    storage = db.relationship("KeyValuePair")

    def __repr__(self):
        return 'Chord node {}, with successor {} and predecessor {}'.format(
                self.hashed_id, self.successor, self.predecessor)

class KeyValuePair(db.Model):
    __tablename__ = 'keyvaluepair'

    id = db.Column(db.Integer, primary_key=True)
    chordnode_id = db.Column(db.Integer, db.ForeignKey('chordnode.id'), nullable=True)
    value = db.Column(db.String)

    def __repr__(self):
        return  '<key-value pair: {}:{}, responsible Chord node: {}'.format(self.id,
                self.value, self.chordnode_id)
