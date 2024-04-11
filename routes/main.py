from flask import Blueprint, render_template, request, jsonify
from ..chatbot.chatbot import chatbot
from ..models.productline import Product_line
from ..db_funcs.bot_conversation import *

main = Blueprint("main", __name__)

#TEST
@main.route("/")
def index():
    return render_template("chat.html")

@main.route("/get", methods=["GET", "POST"])
def chat():
    query = request.form["msg"]
    memory = get_conversation_memory()
    
    _response, memory = get_Chat_response(query, memory)

    update_conversation_memory(memory)

    return _response

#FE API
@main.route("/bot_response", methods=["POST"])
def bot_response():
    try:
        data = request.get_json()
        query = data.get("bot_message")
        
        # Process the query and generate a bot response
        _response, memory = get_Chat_response(query, "")

        # Create a response JSON
        response = {
            "bot_response": _response
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_Chat_response(query, memory):
    bot = chatbot(memory)
    return bot.chat_public(query)
