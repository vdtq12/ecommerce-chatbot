from ..extensions import db

class Supplier(db.Model):
    __tablename__ = 'supplier'

    code = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, unique=True)

    def __init__(self, code, name):
        self.code = code
        self.name = name