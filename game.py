from chesspiece import *
import threading
import board
import struct
import modifiers
import random as rand
from p2p import *
import global_vars
import pygame
from state import *
from textbox import *
from button import *
import time
import os
import json

#colors = ['#a52a2a','#ffffff']
colors = ['#FFDAB9','#008000']
WIDTH = 800
HEIGHT = 800


def printout():
    print("hello world")


class game:
    #root = None
    board = None
    turn_count = 0
    current_square = None
    clicked_square = None
    new_square = None
    turn = "white"
    conn_thread = None
    new_p2p = None
    screen = None
    current_instruction = ""
    running = True
    moved = False
    offer_modifiers = False #Do we offer modifiers this round?
    modifiers = []
    white_king_in_check = False
    black_king_in_check = False
    offer_promotion = False
    endgame = ""




    def __init__(self, conn_type, ip, port):
        self.conn_type = conn_type
        self.ip = ip
        self.port = port
        self.board = board.board(True)
        pygame.init()
        self.conn_thread = threading.Thread(target=self.run_socket)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        #pygame.display.set_caption(f"Chess {self.board.my_color}")
        #TODO:somwhere to join or force join this thread

        self.clicked_square = None
        self.white_king_in_check = False
        self.black_king_in_check = False
        self.move_data = None

    def setup_game(self):
        if(self.conn_type == "connect"):
            self.board.my_color = "black"
            
        else:
            self.board.my_color = "white"

    def get_conn_thread(self):
        return self.conn_thread

#running this function on a separate thread
    def run_socket(self):
        self.new_p2p = p2p(self.conn_type, self.ip, self.port)
        self.new_p2p.init_p2p()
        wait_for_my_move = True
        if(self.conn_type == "connect"):
            wait_for_my_move = False

        while(self.running):
            #send instruction
            if(wait_for_my_move):
                global_vars.send_event.wait()
                if(not self.running):
                    break
                instruction = json.dumps(self.move_data)
                instruction = instruction.encode("utf-8")
                self.new_p2p.send_instruction(instruction)
                global_vars.send_event.clear()
                wait_for_my_move = False
            else:
                #wait for instruction
                instruction = self.new_p2p.recv_instruction() 
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    break
                json_move_data = instruction.decode("utf-8")
                self.move_data = json.loads(json_move_data)
                self.execute_instruction()
                wait_for_my_move = True
        #self.new_p2p.close_all()
        
    def execute_instruction(self):
        #print("Moving a piece from ", i , ", ", j , " to ", current_x, ", ", current_y)
        print("CURRENT INSTRUCTION", self.move_data)
        x0 = self.move_data["x0"]
        y0 = self.move_data["y0"]
        x1 = self.move_data["x1"]
        y1 = self.move_data["y1"]

        
        self.clicked_square = None
        self.board.move_piece(x1,y1,x0,y0,self.turn)
        print("ddf",self.board.chess_array[x0][y0])
        print("ddf",self.board.chess_array[x1][y1])

    #PIECE PROMOTIONN
        piece = self.move_data["promote"] 
        if piece != "":
            self.board.chess_array[x1][y1] = None
            if self.turn =="white":
                self.board.white_pieces.remove((x1,y1))
            if self.turn =="black":
                self.board.black_pieces.remove((x1,y1))
            self.board.add_piece(x1,y1,piece, self.turn)

        #UPGRADE YUH
        mx = self.move_data["mx"]
        my = self.move_data["my"]
        mpiece = self.move_data["mpiece"]
        upgrade = self.move_data["upgrade"]
        debuff  = self.move_data["debuff"]
        if upgrade != "" and mpiece != "":
            modifier = modifiers.lookup[mpiece][upgrade]
            self.board.chess_array[mx][my].upgrades = [modifier.get_capture(),modifier.get_move()]
            self.board.chess_array[mx][my].set_upgrade(modifier)
            self.board.chess_array[mx][my].find_moves(mx,my)
        if debuff != "" and mpiece != "":
            modifier = modifiers.debuff_map[0]
            self.board.chess_array[mx][my].set_debuff(modifier)



        if (self.turn == "black"):
            self.turn_count += 1
        
        white_moves = self.board.update_legal("white")
        black_moves = self.board.update_legal("black")


        if (self.board.is_king_in_check("white")):
            self.white_king_in_check = True
        else: 
            self.white_king_in_check = False
        if (self.board.is_king_in_check("black")):
            self.black_king_in_check = True
        else: 
            self.black_king_in_check = False

        if (white_moves == 0):
            if (self.white_king_in_check):
                self.endgame = "Checkmate! Black Wins"
            else:
                self.endgame = "Stalemate!"
        if (black_moves == 0):
            if (self.black_king_in_check):
                self.endgame = "Checkmate! White Wins"
            else:
                self.endgame = "Stalemate!"
        self.current_square = None

        #print ("The white king is at ", self.board.get_king_location("white"))
        #print ("The black king is at ", self.board.get_king_location("black"))
        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"


    def select_square(self,i,j):
        if (self.board.get_square(i,j) != None):
            self.clicked_square = (i,j)
            piece = self.board.chess_array[i][j]
            print("Starting info for ", i , ",", j)
            #print("Capture: ", piece.possible_Capture)
            #print("Noncapture: ", piece.possible_NonCapture)
            #print(piece.upgrade)
            #print(piece.upgrades)
            print("object.legal ", piece.get_legal_moves())
            print(self.board.get_possible_moves(i,j,piece.get_color()))
            print("board.legal ", self.board.get_legal_moves(i,j))
        #print("selected square ", i , "," , j)
        if (self.moved):
            return
        #print("SELECT SQUARE")
        #print(self.board.white_pieces)
        #print(self.board.black_pieces)
        if(self.turn != self.board.my_color):
            return
        #print("selected square ", i , "," , j)

        if (self.current_square == None):
            if (self.board.get_square(i,j) == None or not(self.board.get_square(i,j).get_color() == self.turn)):
                #print("Invalid square")
                return
            else: #The square you selected must be one of your pieces
                #print("Selected a piece at ", i , "," , j)
                self.current_square = (i,j)

                return
        
        #At this point, you have already selected a piece
        #If you selected another of your piece, swap the current piece to it
        elif (not(self.board.get_square(i,j) == None) and self.board.get_square(i,j).get_color() == self.turn):
            self.current_square = (i,j)
            piece_object = self.board.chess_array[i][j]
            return
        
        #Otherwise, you are attempting to make a move; see if this move is possible, and do it if so
        else:
            current_x, current_y = self.current_square
            new_x, new_y = i, j
            piece_object = self.board.get_square(current_x,current_y)
            piece_name = piece_object.get_name()
            # valid_moves = self.board.get_legal_moves(current_x,current_y)
            valid_moves = piece_object.get_legal_moves()
            print(valid_moves)
            piece_object.set_first_move()
            piece_color = piece_object.get_color()
            wanted_move_xy = (new_x,new_y)
            #print(f"Moving a {piece_color} {piece_name} from {current_x}, {current_y} to {new_x}, {new_y}")
            #print(f"Possible moves {valid_moves} wanted moves {wanted_move_xy}")
            
            # Check if it is a valid move
            if (valid_moves == None):
                #print("Invalid move")
                return
            if wanted_move_xy in valid_moves:
                #print("Valid Move")
                self.move_data = {
                    "x0" : current_x,
                    "y0" : current_y,
                    "x1" : i,
                    "y1" : j,
                    "color" : self.board.my_color,
                    "promote" : "",
                    "mpiece" : "",
                    "upgrade" : "",
                    "debuff" : "",
                    "mx" : "", #since the modifier can be on any piece
                    "my" : ""
                }

                #this is so stupid idk why i still keep this AND USE IT 
                self.current_instruction = struct.pack("iiii5s",i, j, current_x, current_y, bytes(self.board.my_color,"utf-8"))

                if (self.turn_count > 0 and (self.turn_count % 2 == 0)):
                    self.offer_modifiers = True
                else:
                    self.offer_modifiers = False

                if piece_object.name == "p" and i == 7 and piece_object.color == "black":
                    self.offer_promotion = True
                if piece_object.name == "p" and i == 0 and piece_object.color == "white":
                    self.offer_promotion = True
                if not self.offer_modifiers and not self.offer_promotion:
                    self.moved = True
                    self.execute_instruction()

                # while (self.offer_modifiers):
                #     print("Waiting for user to use a powerup")

                #global_vars.send_event.set()
            else: 
                #print("Invalid move")
                return

    def upgrade_callback(self,modifierData):
        randomPiece, modifier,description, idx= modifierData
        print("--R", randomPiece)
        print("--M",modifier)
        print("--D",description)
        
        print(self.board.chess_array[randomPiece[0]][randomPiece[1]].get_name(), " at ", randomPiece[0], ",", randomPiece[1], " is getting modified")

        if not self.offer_promotion:
            self.execute_instruction()
            self.moved = True

        x0 = self.move_data["x0"]
        y0 = self.move_data["y0"]

        x = randomPiece[0]
        y = randomPiece[1]

        if (x == self.move_data["x0"] and y == self.move_data["y0"]):
            x = self.move_data["x1"]
            y = self.move_data["y1"]

        #This means you are buffing one of your pieces
        self.move_data["mpiece"] = self.board.chess_array[x][y].name
        self.move_data["mx"] = x
        self.move_data["my"] = y
        if (self.board.chess_array[x][y].get_color() == self.board.my_color):
            self.board.chess_array[x][y].upgrades = [modifier.get_capture(),modifier.get_move()]
            self.board.chess_array[x][y].set_upgrade(modifier)
            self.board.chess_array[x][y].find_moves(x,y)
            legal_moves = self.board.get_legal_moves(x, y)
            self.board.chess_array[x][y].update_legal_moves(legal_moves)
            #piece bring upgraded
            #upgrade index = 0 since theres only 1 upgrade for every piece right now
            self.move_data["upgrade"] = 0
        else:
            #print("debuffing opponent's piece!")
            self.board.chess_array[randomPiece[0]][randomPiece[1]].set_debuff(modifier)
            #TODO: this is temp
            self.move_data["debuff"] = idx
        self.offer_modifiers = False
        if self.offer_promotion:
            time.sleep(0.5)
        #self.modifiers = []


    def draw_modifiers(self):
        color = (105, 194, 250)

        if (len(self.modifiers) == 0):
            pieces = self.board.white_pieces + self.board.black_pieces
            # if (self.board.my_color == "black"):
            #     my_pieces = self.board.black_pieces
            for piece in pieces.copy():
                pass
                # if (self.board.chess_array[piece[0]][piece[1]].get_name() == "k"):
                #     pieces.remove(piece)
                #if (not (self.board.chess_array[piece[0]][piece[1]].get_name() == "q")):
                #    pieces.remove(piece)
            

            print("======================================")
            for piece in pieces:
                print(piece , " at ", piece[0], ",", piece[1])
            used = []
            for i in range(4):
                randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                x = randomPiece[0]
                y = randomPiece[1]
                square = (x,y)
                
                if (self.board.chess_array[x][y].get_color() == self.board.my_color):
                    while square in used or self.board.chess_array[x][y].get_color() != self.board.my_color:
                    #lol bogo
                        randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                        x = randomPiece[0]
                        y = randomPiece[1]
                        square = (x,y)

                    used.append(square)
                    print(used)

                    powerup = modifiers.get_powerups(self.board.chess_array[x][y].get_name())
                    powerupdescription = "Your " + self.board.chess_array[x][y].get_name() + " at " + chr(ord("a") + y)+ str(8 - x) + powerup.get_description()
                    #print("Power up ", i, " - " , powerupdescription)
                    self.modifiers.append((randomPiece,powerup,powerupdescription,0))
                else:
                    while (self.board.chess_array[x][y].name == "p" or self.board.chess_array[x][y].name == "kn") or square in used or (self.board.chess_array[x][y].get_color() == self.board.my_color):
                    #lol bogo
                        randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                        x = randomPiece[0]
                        y = randomPiece[1]
                        square = (x,y)

                    used.append(square)
                    print(used)

                    idx = modifiers.get_debuff()
                    debuff = modifiers.debuffs[0]
                    debuffdescription = "Your opponent's " + self.board.chess_array[x][y].get_name() + " at " + chr(ord("a") + y)+ str(8 - x)+ debuff.get_description()
                    #print("Debuff ", i, " - " , debuffdescription)
                    self.modifiers.append((randomPiece,debuff,debuffdescription,idx))

        offset = 10
        for i in range(4):
            randomPiece,modifier,description,idx = self.modifiers[i]
            button = text_button(color,(HEIGHT * 0.8 + 5 ),(offset*5 + HEIGHT * i * 0.125 + (i * offset) ),(HEIGHT * 0.2 - 10) ,(HEIGHT * 0.125), 15, description ,self.upgrade_callback, self.modifiers[i])
            button.draw(self.screen)

    def draw_valid(self):
        if(self.clicked_square != None):
            current_x, current_y = self.clicked_square
            piece_object = self.board.get_square(current_x,current_y)
            valid_moves = piece_object.get_legal_moves()
            gray = (150, 150, 150)     
            green = (80, 110, 60)
            blue = (0,0,255)

            if self.board.my_color == "white" and(((8 * current_x) + (current_y )) + (current_x % 2)) % 2 == 0:
                pygame.draw.rect(self.screen, gray, [ (current_y * (HEIGHT * 0.1) ), current_x * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            elif self.board.my_color == "white":
                pygame.draw.rect(self.screen, green, [ (current_y * (HEIGHT * 0.1) ), current_x * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            if self.board.my_color == "black" and(((8 * current_x) + (current_y )) + (current_x % 2)) % 2 == 0:
                pygame.draw.rect(self.screen, gray, [ ((7-current_y) * (HEIGHT * 0.1) ), (7-current_x) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            elif self.board.my_color == "black":
                pygame.draw.rect(self.screen, green, [ ((7-current_y) * (HEIGHT * 0.1) ), (7-current_x) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])

            for move in valid_moves:
                adj_mov = ((8 * move[0]) + move[1])
                if (self.board.my_color == "white"):
                     if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                         pygame.draw.circle(self.screen,gray,[((move[1] * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),move[0] * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                     else:
                         pygame.draw.circle(self.screen,green,[((move[1] * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),move[0] * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                if (self.board.my_color == "black"):
                     if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                         pygame.draw.circle(self.screen,gray,[(((7-move[1]) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-move[0]) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                     else:
                         #pygame.draw.rect(self.screen, green, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7 - move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                         pygame.draw.circle(self.screen,green,[(((7-move[1]) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-move[0]) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            
    
    def draw_selected_info(self):
        if(self.clicked_square != None):
            current_x, current_y = self.clicked_square
            #print("Drawing valid for ", current_x, ",", current_y)
            piece_object = self.board.get_square(current_x,current_y)
            self.screen.blit(piece_object.sprite, (HEIGHT * 0.9, HEIGHT * 0.7))#bro why is this inverted x should always horizontal
            upgrades = "Upgrades: "
            debuffs = "Debuffs: "
            if (piece_object.get_is_upgraded()):
                upgrades += piece_object.get_upgrade_desc()
            else:
                upgrades += "None"
            if (piece_object.get_is_debuffed()):
                debuffs += piece_object.get_debuff_desc()
            else:
                debuffs += "None"
            button = text_button((255,255,255),0,(HEIGHT * 0.8),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,upgrades,None)
            button.hover = False
            button.draw(self.screen)
            button = text_button((255,255,255),0,(HEIGHT * 0.9),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,debuffs,None)
            button.hover = False
            button.draw(self.screen)

    def draw_grid(self):
        font = pygame.font.Font(None, 25) 
        #if (self.board.my_color == "white"):
        for i in range (8):
            if self.board.my_color == "black":
                text_surf = font.render(str(1 + i), True, "black")
                rect = text_surf.get_rect(center=(10, HEIGHT*.1 * i + (HEIGHT*0.015)))
                self.screen.blit(text_surf, rect)

                text_surf = font.render(str(chr(ord("h") - i)), True, "black")
                rect = text_surf.get_rect(center=(WIDTH*.1 * i - 10+ WIDTH*.1,HEIGHT*.8 - 10))
                self.screen.blit(text_surf, rect)
            if self.board.my_color == "white":
                text_surf = font.render(str(8 - i), True, "black")
                rect = text_surf.get_rect(center=(10, HEIGHT*.1 * i + (HEIGHT*0.015)))
                self.screen.blit(text_surf, rect)

                text_surf = font.render(str(chr(ord("a") + i)), True, "black")
                rect = text_surf.get_rect(center=(WIDTH*.1 * i - 10+ WIDTH*.1,HEIGHT*.8 - 10))
                self.screen.blit(text_surf, rect)
 
    def draw_captured(self):
        pass
    def draw_pieces(self):
        uparrow = pygame.transform.scale(pygame.image.load("resources/uparrow.png"), (30,30))
        downarrow = pygame.transform.scale(pygame.image.load("resources/downarrow.png"), (30,30))
        if (self.board.my_color == "white"):
            #print ("white", len(self.board.white_pieces), " - ", len(self.board.black_pieces))
            for x,y in self.board.white_pieces:
                piece = self.board.chess_array[x][y]
                self.screen.blit(piece.sprite, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_upgraded()):
                    self.screen.blit(uparrow, (y * (HEIGHT * 0.1) + 50, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_debuffed()):
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for x,y in self.board.black_pieces:
                piece = self.board.chess_array[x][y]
                self.screen.blit(piece.sprite, (y *(HEIGHT * 0.1) , x  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_is_upgraded()):
                    self.screen.blit(uparrow, (y * (HEIGHT * 0.1) + 50, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_debuffed()):
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
        else:
            #print ("black", len(self.board.white_pieces), " - ", len(self.board.black_pieces))
            for i in range(len(self.board.white_pieces)):
                x = self.board.white_pieces[i][0]
                y = self.board.white_pieces[i][1]
                piece = self.board.chess_array[x][y]
                self.screen.blit(piece.sprite, ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_upgraded()):
                    self.screen.blit(uparrow,  ((7-y) * (HEIGHT * 0.1) + 50, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_debuffed()):
                    self.screen.blit(downarrow,  ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for i in range(len(self.board.black_pieces)):
                x = self.board.black_pieces[i][0]
                y = self.board.black_pieces[i][1]
                piece = self.board.chess_array[x][y]
                self.screen.blit(piece.sprite, ((7-y) *(HEIGHT * 0.1) , (7-x)  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_is_upgraded()):
                    self.screen.blit(uparrow,  ((7-y) * (HEIGHT * 0.1) + 50, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_is_debuffed()):
                    self.screen.blit(downarrow,  ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal

    def draw_board(self):
        for i in range(32):
            column = i % 4
            row = i // 4
            color = (255,255,255)
            if row % 2 == 0:
                #Screen, color, LH corner, RH corner
                pygame.draw.rect(self.screen, color, [ (HEIGHT * 0.6) - (column * (HEIGHT * 0.2) ), row * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            else:
                pygame.draw.rect(self.screen, color, [ (HEIGHT * 0.7) - (column * (HEIGHT * 0.2)), row *(HEIGHT * 0.1) ,(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            button = text_button((255,255,255),0,(HEIGHT * 0.8),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,"",None)
            button.hover = False
            button.draw(self.screen)
            button = text_button((255,255,255),0,(HEIGHT * 0.9),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,"",None)
            button.hover = False
            button.draw(self.screen)
            #pygame.draw.rect(self.screen, 'white', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)])
            #pygame.draw.rect(self.screen, 'gray', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)], 5)
            #pygame.draw.rect(self.screen, 'gold', [(HEIGHT * 0.8), 0, (HEIGHT * 0.8), (HEIGHT * 0.8)], 5)
            status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                        'Black: Select a Piece to Move!', 'Black: Select a Destination!']
            self.draw_valid()
            for i in range(9):
                pygame.draw.line(self.screen, 'black', (0,(HEIGHT * 0.1)  * i), ((HEIGHT * 0.8),(HEIGHT * 0.1) * i), 2)
                pygame.draw.line(self.screen, 'black', ((HEIGHT * 0.1)* i, 0), ((HEIGHT * 0.1)* i, (HEIGHT * 0.8)), 2)
        red = (255,0,0)
        if (self.white_king_in_check):
            x,y = self.board.get_king_location("white")
            if (self.board.my_color == "white"):
                pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            if (self.board.my_color == "black"):
                pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
        if (self.black_king_in_check):
            x,y = self.board.get_king_location("black")
            if (self.board.my_color == "white"):
                pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            if (self.board.my_color == "black"):
                pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)

    #promotion callback

    def promote(self, x,y,piece):
        self.board.chess_array[x][y] = None
        if self.board.my_color =="white":
            self.board.white_pieces.remove((x,y))
        if self.board.my_color =="black":
            self.board.black_pieces.remove((x,y))
        self.board.add_piece(x,y,piece, self.board.my_color)
        self.move_data["promote"] = piece
        self.offer_promotion = False
        self.moved = True
        self.execute_instruction()

    def draw_promotion_options(self):
    
        i = self.move_data["x0"]
        j = self.move_data["y0"]

        offset = 10

        font = pygame.font.Font(None, 36) 
        if (self.board.my_color == "black"):
            options = ["resources/Chess_ndt60.png", "resources/Chess_rdt60.png", "resources/Chess_bdt60.png", "resources/Chess_qdt60.png"]
            n = ["kn", "r", "b", "q"]
            for k in range(2,6):
                piece_background = text_button((150,150,150),(HEIGHT * 0.85) , (HEIGHT * k * 0.1 + offset * k),(HEIGHT * 0.1),(HEIGHT * 0.1) ,0, "",None)
                piece_background.draw(self.screen)
                piece_promote = image_button((HEIGHT * 0.85) , (HEIGHT * k * 0.1 + offset * k),(HEIGHT * 0.1) ,(HEIGHT * 0.1), options[k-2],1, self.promote, i,j,n[k-2])
                piece_promote.draw(self.screen)
        if (self.board.my_color == "white"):
            options = ["resources/Chess_nlt60.png", "resources/Chess_rlt60.png", "resources/Chess_blt60.png", "resources/Chess_qlt60.png"]
            n = ["kn", "r", "b", "q"]
            for k in range(2,6):
                piece_promote = image_button((HEIGHT * 0.8) , (HEIGHT * k * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1), options[k-2],1, self.promote, i,j,n[k-2])
                piece_promote.draw(self.screen)
        return True
        

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.endgame == "":
                    if (event.pos[0] < 0.8 * WIDTH and event.pos[1] < 0.8 * WIDTH):
                        if (self.board.my_color == "white"):
                            self.select_square(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
                        else:
                            self.select_square(7 - event.pos[1] // (WIDTH // 10),7 - event.pos[0] // (WIDTH // 10))

            self.screen.fill((105,146,62))
            self.draw_board()
            self.draw_pieces()
            if self.offer_modifiers:
                self.draw_modifiers()
            else:
                self.modifiers = []

            self.draw_grid()
            self.draw_selected_info()
            if not self.offer_modifiers and self.offer_promotion:
                self.draw_promotion_options()
            if self.endgame != "":
                color = (105, 194, 250)
                button = text_button(color,(HEIGHT * 0.2),(HEIGHT * 0.3) ,(HEIGHT * 0.4), (HEIGHT * 0.2),50,self.endgame,None)
                button.hover = False
                button.draw(self.screen)

            #self.draw_promotion_options()
            #print("Offering modifiers is ", self.offer_modifiers, " because ", self.turn_count)
            pygame.display.flip()

            #if (self.moved and not(self.offer_modifiers)):

            if (self.moved and not(self.offer_modifiers)):
                #print("Sending Move")
                global_vars.send_event.set()
                self.moved = False

            #self.draw_captured()

        pygame.display.quit()
        pygame.quit()
        global_vars.send_event.set()

    def main_loop_menu(self):
        state = "main menu"
#for main menu
        scale = 5
        button_x_pos = (WIDTH// 2) - (57*scale // 2)
        height_offset = 50
        host_button = image_button(button_x_pos,HEIGHT//2 - height_offset, 57,9, "resources/create_game_button.png",scale, None)
        join_button =  image_button(button_x_pos,HEIGHT//2 + height_offset,57,9, "resources/join_game_button.png",scale, None)
        textbox_width = 350
        textbox_height = 50
#for joining game menu
        #TODO:add color pallete globals cuz this shits getting ugly
        ip_textbox = Textbox((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 - height_offset, textbox_width,textbox_height, textbox_height-8, "ip")
        port_textbox = Textbox((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 + height_offset, textbox_width,textbox_height, textbox_height-8, "port")
        connect_button = text_button((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 + 3*height_offset, textbox_width,textbox_height, textbox_height-8, "join game",None)
        while self.running:
            eventlist = pygame.event.get()
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            if state == "main menu":
                self.screen.fill((172,200,255))
                if host_button.draw(self.screen) == 1:
                    state = "host game"
                if join_button.draw(self.screen) == 1:
                    state = "join game"

            elif state == "host game":
                self.conn_type = "host"
                self.ip = "0.0.0.0"
                self.port = 2020 #TODO: display a selected available port
                state = "play game"
                self.setup_game()
                self.conn_thread.start()

            elif state == "join game":
                self.conn_type = "connect"
                self.screen.fill((172,200,255))
                self.ip = ip_textbox.handle_textbox(self.screen, eventlist)
                port = port_textbox.handle_textbox(self.screen, eventlist)

                if(connect_button.draw(self.screen) == 1):
                    is_num = True
                    for char in port:
                        if not char.isdigit():
                            is_num = False
                            break
                    if is_num:
                        self.port = int(port)
                    state = "play game"
                    #self.conn_thread = threading.Thread(target=self.run_socket)
                    self.setup_game()
                    self.conn_thread.start()

            elif state == "play game":
                self.main_loop()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        global_vars.send_event.set()
