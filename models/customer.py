from ..extensions import db

class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.String, primary_key=True, nullable=False)
    cart_id = db.Column(db.BigInteger)
    
    bot_dialogues = db.relationship("Bot_dialogue", backref="sender_id", cascade="all, delete-orphan")

    def __init__(self, id, cart_id=None):
        self.id = id
        self.cart_id = cart_id