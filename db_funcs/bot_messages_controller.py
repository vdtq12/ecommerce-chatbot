from ..extensions import db
from ..models.botmessages import Bot_messages
from datetime import datetime

def get_dialogue_messages_by_id(dialogue_id):
    try:
        messages = Bot_messages.query.filter_by(dialogue=dialogue_id).all()
        if not messages:
            return None

        dialogue_messages = []
        for message in messages:
            dialogue_messages.append(message.to_dict())
        return dialogue_messages
    except Exception as e:
        # Handle any exceptions that occur during the retrieval process
        print(f"Error: {str(e)}")
        return []
    
def add_dialogue_message(dialogue_id, content, bot_answer):
    try:
        new_message = Bot_messages(dialogue=dialogue_id, created_at=datetime.now(), content=content, bot_answer=bot_answer)
        db.session.add(new_message)
        db.session.commit()
        return {"message": "Dialogue message updated successfully"}
    except Exception as e:
        # Handle any exceptions that occur during the update process
        print(f"Error: {str(e)}")
        return {"error": "Failed to update dialogue message"}