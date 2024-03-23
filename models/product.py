from ..extensions import db


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String(10), unique=True)
    images = db.Column(db.ARRAY(db.String))
    local_specs = db.Column(db.JSON)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float)
    is_standard = db.Column(db.Boolean, default=False)
    product_line = db.Column(
        db.Integer,
        db.ForeignKey(
            "product_line.product_id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )

    def __init__(self, name, quantity, price, local_specs):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.local_specs = local_specs
