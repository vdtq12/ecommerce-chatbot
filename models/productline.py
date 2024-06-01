from ..extensions import db


class Product_line(db.Model):
    __tablename__ = "product_line"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(
        db.Text,
        db.ForeignKey(
            "category.category_name", ondelete="SET NULL", onupdate="CASCADE"
        ),
        nullable=True,
    )
    vendor = db.Column(
        db.Text,
        db.ForeignKey("vendor.code", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    name = db.Column(db.String(30), nullable=False)
    # description = db.Column(db.Text, default="Đang cập nhật")

    def __init__(self, category, vendor, name, description="Đang cập nhật"):
        self.category = category
        self.vendor = vendor
        self.name = name
        # self.description = description
