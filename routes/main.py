from flask import Blueprint, render_template, request, jsonify
from ..chatbot.chatbot import chatbot
from ..db_funcs.bot_dialogue_controller import *
from ..db_funcs.bot_messages_controller import *
from flask_cors import cross_origin

main = Blueprint("main", __name__)

#TEST
@main.route("/")
@cross_origin()
def index():
    return render_template("chat.html")

@main.route("/get", methods=["GET", "POST"])
@cross_origin()
def chat():
    query = request.form["msg"]
    # memory = get_conversation_memory()
    
    _response, memory = get_Chat_response(query, memory)

    # update_conversation_memory(memory)

    return _response

#FE API

#get the chatbot response
@main.route("/bot_response", methods=["POST"])
@cross_origin()
def bot_response():
    try:
        data = request.get_json()
        query = data.get("customer_message")
        current_dialogue = get_dialogue(data.get("customer_id"))
        if not current_dialogue:
            current_dialogue = create_dialogue(data.get("customer_id"))
        
        # Process the query and generate a bot response
        _response, new_summary = get_Chat_response(query, current_dialogue.summary)

        # Update summary
        update_dialogue_summary(current_dialogue.id, new_summary)
        add_dialogue_message(current_dialogue.id, query, _response)

        # Create a response JSON
        new_dialogue = get_dialogue(data.get("customer_id"))
        response = {
            "bot_response": _response,
            "dialogue": new_dialogue.to_dict()
        }

        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get the dialogue messages content by id
@main.route("/dialogue/<int:dialogue_id>", methods=["GET"])
@cross_origin()
def get_dialogue_messages(dialogue_id):
    try:
        dialogue_messages = get_dialogue_messages_by_id(dialogue_id)
        if not dialogue_messages:
            return jsonify({"error": "Dialogue not found"}), 404

        response = {
            "id": dialogue_id,
            "messages": dialogue_messages
        }
        return jsonify(response), 200
    except Exception as e:
        # Handle any exceptions that occur during the retrieval process
        return jsonify({"error": str(e)}), 500

#clear dialogue context
@main.route("/dialogue/<int:dialogue_id>", methods=["DELETE"])
@cross_origin()
def clear_dialogue_context(dialogue_id):
    try:
        clearFlag = clear_context(dialogue_id)
        if clearFlag == 1:
            return jsonify({"message": f"Dialogue context cleared for dialogue ID {dialogue_id}"}), 200
        elif clearFlag == -1:
            return jsonify({"error": "Dialogue not found"}), 404
        elif clearFlag == -2:
            return jsonify({"error": "The context of this dialogue has been cleared before"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#get latest dialogue
@main.route("/dialogue/latest/<string:customer_id>", methods=["GET"])
@cross_origin()
def get_latest_dialogue_messages(customer_id):
    try:
        latest_dialogue = get_dialogue(customer_id)

        if not latest_dialogue:
            return jsonify({"error": "No dialogue found"}), 404

        latest_dialogue_messages = get_dialogue_messages_by_id(latest_dialogue.id)

        # Create a response JSON
        response = {
            "dialogue": latest_dialogue.to_dict(),
            "messages": latest_dialogue_messages
        }

        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get all dialogues
@main.route("/dialogue/all/<string:customer_id>", methods=["GET"])
@cross_origin()
def get_all_dialogues(customer_id):
    try:
        dialogues = get_all_dialogue(customer_id)

        if not dialogues:
            return jsonify({"error": "No customer found"}), 404

        # Create a response JSON
        response = {
            "dialogue": dialogues,
        }

        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_Chat_response(query, memory):
    bot = chatbot(memory)
    return bot.chat_public(query)
