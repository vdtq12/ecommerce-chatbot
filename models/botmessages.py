from ..extensions import db

class Bot_messages(db.Model):
    __tablename__ = "bot_messages"

    dialogue = db.Column(db.Integer, db.ForeignKey("bot_dialogue.id", ondelete="CASCADE"), primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    bot_answer = db.Column(db.Text)

    def __init__(self, dialogue, created_at, content, bot_answer=None):
        self.dialogue = dialogue
        self.created_at = created_at
        self.content = content
        self.bot_answer = bot_answer

    def to_dict(self):
        return {
            "create_at": self.created_at.isoformat(),
            "user_message": self.content,
            "bot_message": self.bot_answer
        }