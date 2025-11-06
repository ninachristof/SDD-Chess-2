from button import *
from textbox import *
WIDTH = 800 #TODO: put these in global file
HEIGHT = 800
class state():

    name = ""
    object_handlers = []
    handle_state = None
    prev_state = None
    next_state = None

    def __init__(self, name, callback):
        self.name = name
        self.handle_state = callback
    def get_next_state(self):
        return self.next_state
    def run_object_handlers(self, screen, eventlist):
        for handler in object_handler:
            handler(screen, eventlist)

def handle_main_menu(screen):
    screen.fill((172,200,255))

def handle_join_game(screen, eventlist):
    screen.fill((172,200,255))



#def init_state_machine():
#
#    scale = 5
#    button_x_pos = (WIDTH// 2) - (57*scale // 2)
#    height_offset = 50
#    start_button = Button(button_x_pos,HEIGHT//2 - height_offset,"create button", None,"resources/create_game_button.png",57,9,scale)
#    join_button = Button(button_x_pos,HEIGHT//2 + height_offset,"join button", None,"resources/join_game_button.png",57,9,scale)
#
#    main_menu_state = state("main_menu", handle_main_menu)
#
#    main_menu_state.object_handlers.append(start_button.draw)
#    main_menu_state.object_handers.append(join_button.draw)
#
#    create_game_state = state("create_game",None)
#
#    join_game_state = state("join_game", None)
#
#    textbox = Textbox((100,100,100), WIDTH//2, HEIGHT//2, 400,50, 50)
#    join_game_state.object_handlers.append(textbox.handle_textbox)
#    return main_menu_state
#      
