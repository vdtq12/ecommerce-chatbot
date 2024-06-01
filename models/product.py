from ..extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String(10), unique=True)
    local_specs = db.Column(db.JSON)
    quantity = db.Column(db.Integer, default=1)
    list_price  = db.Column(db.Float)
    product_line = db.Column(
        db.Integer,
        db.ForeignKey(
            "product_line.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )

    def __init__(self, name, quantity, list_price , local_specs):
        self.name = name
        self.quantity = quantity
        self.list_price  = list_price 
        self.local_specs = local_specs

    def to_dict(self):
        return {
            'name': self.name,
            'local_specs': self.local_specs,
        }
