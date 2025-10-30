import threading
def init_vars():
    global current_instruction
    current_instruction = ""
    global send_event
    send_event = threading.Event()
