from flask import Blueprint, render_template, request
from ..chatbot.chatbot import chatbot
from ..models.productline import Product_line
from ..db_funcs.bot_conversation import *

main = Blueprint("main", __name__)

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

def get_Chat_response(query, memory):
    bot = chatbot(memory)
    return bot.chat_public(query)
