from ..extensions import db

class Bot_dialogue(db.Model):
    __tablename__ = "bot_dialogue"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    sender = db.Column(db.String, db.ForeignKey("customer.id", ondelete="CASCADE"), nullable=False)
    deleted_at = db.Column(db.DateTime(timezone=True))
    summary = db.Column(db.Text)

    messages = db.relationship("Bot_messages", backref="dialogue_id", cascade="all, delete-orphan")

    def __init__(self, created_at, sender, summary=""):
        self.created_at = created_at
        self.sender = sender
        self.summary = summary

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'sender': self.sender,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'summary': self.summary
        }