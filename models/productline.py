from ..extensions import db


class Product_line(db.Model):
    __tablename__ = "product_line"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(
        db.Text,
        db.ForeignKey(
            "category.category_name", ondelete="SET NULL", onupdate="CASCADE"
        ),
        nullable=True,
    )
    supplier = db.Column(
        db.Text,
        db.ForeignKey("supplier.code", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    name = db.Column(db.String(30), nullable=False)
    # description = db.Column(db.Text, default="Đang cập nhật")

    def __init__(self, category, supplier, name, description="Đang cập nhật"):
        self.category = category
        self.supplier = supplier
        self.name = name
        # self.description = description
