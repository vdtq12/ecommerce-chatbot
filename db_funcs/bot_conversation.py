memory = ""

def get_conversation_memory():
    return memory

def update_conversation_memory(mem: str):
    global memory
    memory += mem