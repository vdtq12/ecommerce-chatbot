from ..extensions import db

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name