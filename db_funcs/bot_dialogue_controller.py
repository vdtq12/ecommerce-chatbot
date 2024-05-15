from ..extensions import db
from ..models.botdialogue import Bot_dialogue
from datetime import datetime

def get_dialogue(customer_id):
    dialogue = Bot_dialogue.query.filter_by(sender=customer_id, deleted_at=None).first()
    if dialogue:
        return dialogue
    else:
        return None
    
def get_all_dialogue(customer_id):
    dialogues = Bot_dialogue.query.filter_by(sender=customer_id).order_by(Bot_dialogue.id.asc()).all()
    if not dialogues:
        return None

    dialogues_response = []
    for dialogue in dialogues:
        dialogues_response.append(dialogue.to_dict())
    return dialogues_response
    
def create_dialogue(customer_id):
    new_dialogue = Bot_dialogue(created_at=datetime.now(), sender=customer_id)
    db.session.add(new_dialogue)
    db.session.commit()
    return new_dialogue

def update_dialogue_summary(dialogue_id, new_summary):
    dialogue = Bot_dialogue.query.get(dialogue_id)
    if dialogue:
        dialogue.summary = new_summary
        db.session.commit()
        return True
    else:
        return False
    
def clear_context(dialogue_id):
    dialogue = Bot_dialogue.query.get(dialogue_id)

    if dialogue:
        if dialogue.deleted_at:
            return -2  #context has been cleared before
        dialogue.deleted_at = datetime.now()
        db.session.commit()
        return 1 #OK
    else:
        return -1 #No dialogue found