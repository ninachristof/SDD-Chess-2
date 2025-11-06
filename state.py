from button import *
WIDTH = 800 #TODO: put these in global file
HEIGHT = 800
class state():

    name = ""
    handle_state = None
    prev_state = None
    next_state = None

    def __init__(self, name, callback):
        self.name = name
        self.handle_state = callback

def handle_main_menu(screen):
    screen.fill((172,200,255))
    scale = 5
    button_x_pos = (WIDTH// 2) - (57*scale // 2)
    height_offset = 50
   
    print(button_x_pos)
    start_button = Button(button_x_pos,HEIGHT//2 - height_offset,"create button", None,"resources/create_game_button.png",57,9,scale)
    join_button = Button(button_x_pos,HEIGHT//2 + height_offset,"join button", None,"resources/join_game_button.png",57,9,scale)
    start_button.draw(screen)
    join_button.draw(screen)

def init_state_machine():
    main_menu_state = state("main_menu", handle_main_menu)
    create_game_state = state("create_game",None)
    join_game_state = state("join_game", None)
    return main_menu_state
      
