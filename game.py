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
    turnCount = 0
    currentSquare = None
    clickedSquare = None
    newSquare = None
    turn = "white"
    conn_thread = None
    new_p2p = None
    screen = None
    current_instruction = ""
    running = True
    moved = False
    offermodifiers = False #Do we offer modifiers this round?
    modifiers = []
    whitekinginCheck = False
    blackkinginCheck = False
    offerpromotion = False
    endgame = ""




    def __init__(self, conn_type, ip, port):
        self.conn_type = conn_type
        self.ip = ip
        self.port = port
        self.board = board.board(True)
        pygame.init()
        self.conn_thread = threading.Thread(target=self.run_socket)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        #pygame.display.set_caption(f"Chess {self.board.mycolor}")
        #TODO:somwhere to join or force join this thread

        self.clickedSquare = None
        self.whitekinginCheck = False
        self.blackkinginCheck = False
        self.move_data = None

    def setup_game(self):
        if(self.conn_type == "connect"):
            self.board.mycolor = "black"
            
        else:
            self.board.mycolor = "white"

    def get_conn_thread(self):
        return self.conn_thread

#running this function on a separate thread
    def run_socket(self):
        self.new_p2p = p2p(self.conn_type, self.ip, self.port)
        self.new_p2p.initP2p()
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
                self.new_p2p.sendInstruction(instruction)
                global_vars.send_event.clear()
                wait_for_my_move = False
            else:
                #wait for instruction
                instruction = self.new_p2p.recvInstruction() 
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    break
                json_move_data = instruction.decode("utf-8")
                self.move_data = json.loads(json_move_data)
                self.execute_instruction()
                wait_for_my_move = True
        #self.new_p2p.close_all()
        
    def execute_instruction(self):
        #print("Moving a piece from ", i , ", ", j , " to ", currentX, ", ", currentY)
        print("CURRENT INSTRUCTION", self.move_data)
        x0 = self.move_data["x0"]
        y0 = self.move_data["y0"]
        x1 = self.move_data["x1"]
        y1 = self.move_data["y1"]

        
        self.clickedSquare = None
        self.board.movePiece(x1,y1,x0,y0,self.turn)
        print("ddf",self.board.chessArray[x0][y0])
        print("ddf",self.board.chessArray[x1][y1])

    #PIECE PROMOTIONN
        piece = self.move_data["promote"] 
        if piece != "":
            self.board.chessArray[x1][y1] = None
            if self.turn =="white":
                self.board.whitePieces.remove((x1,y1))
            if self.turn =="black":
                self.board.blackPieces.remove((x1,y1))
            self.board.addPiece(x1,y1,piece, self.turn)

        #UPGRADE YUH
        mx = self.move_data["mx"]
        my = self.move_data["my"]
        mpiece = self.move_data["mpiece"]
        upgrade = self.move_data["upgrade"]
        debuff  = self.move_data["debuff"]
        if upgrade != "" and mpiece != "":
            modifier = modifiers.lookup[mpiece][upgrade]
            self.board.chessArray[mx][my].upgrades = [modifier.get_capture(),modifier.get_move()]
            self.board.chessArray[mx][my].set_upgrade(modifier)
            self.board.chessArray[mx][my].findMoves(mx,my)
        if debuff != "" and mpiece != "":
            modifier = modifiers.debuff_map[0]
            self.board.chessArray[mx][my].set_debuff(modifier)



        if (self.turn == "black"):
            self.turnCount += 1
        
        whiteMoves = self.board.updateLegal("white")
        blackMoves = self.board.updateLegal("black")


        if (self.board.isKinginCheck("white")):
            self.whitekinginCheck = True
        else: 
            self.whitekinginCheck = False
        if (self.board.isKinginCheck("black")):
            self.blackkinginCheck = True
        else: 
            self.blackkinginCheck = False

        if (whiteMoves == 0):
            if (self.whitekinginCheck):
                self.endgame = "Checkmate! Black Wins"
            else:
                self.endgame = "Stalemate!"
        if (blackMoves == 0):
            if (self.blackkinginCheck):
                self.endgame = "Checkmate! White Wins"
            else:
                self.endgame = "Stalemate!"
        self.currentSquare = None

        #print ("The white king is at ", self.board.getKingLocation("white"))
        #print ("The black king is at ", self.board.getKingLocation("black"))
        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"


    def selectsquare(self,i,j):
        if (self.board.getSquare(i,j) != None):
            self.clickedSquare = (i,j)
            piece = self.board.chessArray[i][j]
            print("Starting info for ", i , ",", j)
            #print("Capture: ", piece.possible_Capture)
            #print("Noncapture: ", piece.possible_NonCapture)
            #print(piece.upgrade)
            #print(piece.upgrades)
            print("object.legal ", piece.getlegalMoves())
            print(self.board.getPossibleMoves(i,j,piece.get_color()))
            print("board.legal ", self.board.getLegalMoves(i,j))
        #print("selected square ", i , "," , j)
        if (self.moved):
            return
        #print("SELECT SQUARE")
        #print(self.board.whitePieces)
        #print(self.board.blackPieces)
        if(self.turn != self.board.mycolor):
            return
        #print("selected square ", i , "," , j)

        if (self.currentSquare == None):
            if (self.board.getSquare(i,j) == None or not(self.board.getSquare(i,j).get_color() == self.turn)):
                #print("Invalid square")
                return
            else: #The square you selected must be one of your pieces
                #print("Selected a piece at ", i , "," , j)
                self.currentSquare = (i,j)

                return
        
        #At this point, you have already selected a piece
        #If you selected another of your piece, swap the current piece to it
        elif (not(self.board.getSquare(i,j) == None) and self.board.getSquare(i,j).get_color() == self.turn):
            self.currentSquare = (i,j)
            pieceObject = self.board.chessArray[i][j]
            return
        
        #Otherwise, you are attempting to make a move; see if this move is possible, and do it if so
        else:
            currentX, currentY = self.currentSquare
            newX, newY = i, j
            pieceObject = self.board.getSquare(currentX,currentY)
            pieceName = pieceObject.get_name()
            # validMoves = self.board.getLegalMoves(currentX,currentY)
            validMoves = pieceObject.getlegalMoves()
            print(validMoves)
            pieceObject.set_first_move()
            pieceColor = pieceObject.get_color()
            wantedMoveXY = (newX,newY)
            #print(f"Moving a {pieceColor} {pieceName} from {currentX}, {currentY} to {newX}, {newY}")
            #print(f"Possible moves {validMoves} wanted moves {wantedMoveXY}")
            
            # Check if it is a valid move
            if (validMoves == None):
                #print("Invalid move")
                return
            if wantedMoveXY in validMoves:
                #print("Valid Move")
                self.move_data = {
                    "x0" : currentX,
                    "y0" : currentY,
                    "x1" : i,
                    "y1" : j,
                    "color" : self.board.mycolor,
                    "promote" : "",
                    "mpiece" : "",
                    "upgrade" : "",
                    "debuff" : "",
                    "mx" : "", #since the modifier can be on any piece
                    "my" : ""
                }

                #this is so stupid idk why i still keep this AND USE IT 
                self.current_instruction = struct.pack("iiii5s",i, j, currentX, currentY, bytes(self.board.mycolor,"utf-8"))

                if (self.turnCount > 0 and (self.turnCount % 2 == 0)):
                    self.offermodifiers = True
                else:
                    self.offermodifiers = False

                if pieceObject.name == "p" and i == 7 and pieceObject.color == "black":
                    self.offerpromotion = True
                if pieceObject.name == "p" and i == 0 and pieceObject.color == "white":
                    self.offerpromotion = True
                if not self.offermodifiers and not self.offerpromotion:
                    self.moved = True
                    self.execute_instruction()

                # while (self.offermodifiers):
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
        
        print(self.board.chessArray[randomPiece[0]][randomPiece[1]].get_name(), " at ", randomPiece[0], ",", randomPiece[1], " is getting modified")

        if not self.offerpromotion:
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
        self.move_data["mpiece"] = self.board.chessArray[x][y].name
        self.move_data["mx"] = x
        self.move_data["my"] = y
        if (self.board.chessArray[x][y].get_color() == self.board.mycolor):
            self.board.chessArray[x][y].upgrades = [modifier.get_capture(),modifier.get_move()]
            self.board.chessArray[x][y].set_upgrade(modifier)
            self.board.chessArray[x][y].findMoves(x,y)
            legalMoves = self.board.getLegalMoves(x, y)
            self.board.chessArray[x][y].updateLegalMoves(legalMoves)
            #piece bring upgraded
            #upgrade index = 0 since theres only 1 upgrade for every piece right now
            self.move_data["upgrade"] = 0
        else:
            #print("debuffing opponent's piece!")
            self.board.chessArray[randomPiece[0]][randomPiece[1]].set_debuff(modifier)
            #TODO: this is temp
            self.move_data["debuff"] = idx
        self.offermodifiers = False
        if self.offerpromotion:
            time.sleep(0.5)
        #self.modifiers = []


    def draw_modifiers(self):
        color = (105, 194, 250)

        if (len(self.modifiers) == 0):
            pieces = self.board.whitePieces + self.board.blackPieces
            # if (self.board.mycolor == "black"):
            #     my_pieces = self.board.blackPieces
            for piece in pieces.copy():
                pass
                # if (self.board.chessArray[piece[0]][piece[1]].get_name() == "k"):
                #     pieces.remove(piece)
                #if (not (self.board.chessArray[piece[0]][piece[1]].get_name() == "q")):
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
                
                if (self.board.chessArray[x][y].get_color() == self.board.mycolor):
                    while square in used or self.board.chessArray[x][y].get_color() != self.board.mycolor:
                    #lol bogo
                        randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                        x = randomPiece[0]
                        y = randomPiece[1]
                        square = (x,y)

                    used.append(square)
                    print(used)

                    powerup = modifiers.getPowerups(self.board.chessArray[x][y].get_name())
                    powerupdescription = "Your " + self.board.chessArray[x][y].get_name() + " at " + chr(ord("a") + y)+ str(8 - x) + powerup.get_description()
                    #print("Power up ", i, " - " , powerupdescription)
                    self.modifiers.append((randomPiece,powerup,powerupdescription,0))
                else:
                    while (self.board.chessArray[x][y].name == "p" or self.board.chessArray[x][y].name == "kn") or square in used or (self.board.chessArray[x][y].get_color() == self.board.mycolor):
                    #lol bogo
                        randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                        x = randomPiece[0]
                        y = randomPiece[1]
                        square = (x,y)

                    used.append(square)
                    print(used)

                    idx = modifiers.getDebuff()
                    debuff = modifiers.debuffs[0]
                    debuffdescription = "Your opponent's " + self.board.chessArray[x][y].get_name() + " at " + chr(ord("a") + y)+ str(8 - x)+ debuff.get_description()
                    #print("Debuff ", i, " - " , debuffdescription)
                    self.modifiers.append((randomPiece,debuff,debuffdescription,idx))

        offset = 10
        for i in range(4):
            randomPiece,modifier,description,idx = self.modifiers[i]
            button = TextButton(color,(HEIGHT * 0.8 + 5 ),(offset*5 + HEIGHT * i * 0.125 + (i * offset) ),(HEIGHT * 0.2 - 10) ,(HEIGHT * 0.125), 15, description ,self.upgrade_callback, self.modifiers[i])
            button.draw(self.screen)

    def draw_valid(self):
        if(self.clickedSquare != None):
            currentX, currentY = self.clickedSquare
            pieceObject = self.board.getSquare(currentX,currentY)
            validMoves = pieceObject.getlegalMoves()
            gray = (150, 150, 150)     
            green = (80, 110, 60)
            blue = (0,0,255)

            if self.board.mycolor == "white" and(((8 * currentX) + (currentY )) + (currentX % 2)) % 2 == 0:
                pygame.draw.rect(self.screen, gray, [ (currentY * (HEIGHT * 0.1) ), currentX * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            elif self.board.mycolor == "white":
                pygame.draw.rect(self.screen, green, [ (currentY * (HEIGHT * 0.1) ), currentX * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            if self.board.mycolor == "black" and(((8 * currentX) + (currentY )) + (currentX % 2)) % 2 == 0:
                pygame.draw.rect(self.screen, gray, [ ((7-currentY) * (HEIGHT * 0.1) ), (7-currentX) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
            elif self.board.mycolor == "black":
                pygame.draw.rect(self.screen, green, [ ((7-currentY) * (HEIGHT * 0.1) ), (7-currentX) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])

            for move in validMoves:
                adj_mov = ((8 * move[0]) + move[1])
                if (self.board.mycolor == "white"):
                     if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                         pygame.draw.circle(self.screen,gray,[((move[1] * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),move[0] * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                     else:
                         pygame.draw.circle(self.screen,green,[((move[1] * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),move[0] * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                if (self.board.mycolor == "black"):
                     if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                         pygame.draw.circle(self.screen,gray,[(((7-move[1]) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-move[0]) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                     else:
                         #pygame.draw.rect(self.screen, green, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7 - move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                         pygame.draw.circle(self.screen,green,[(((7-move[1]) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-move[0]) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            
    
    def draw_selected_info(self):
        if(self.clickedSquare != None):
            currentX, currentY = self.clickedSquare
            #print("Drawing valid for ", currentX, ",", currentY)
            pieceObject = self.board.getSquare(currentX,currentY)
            self.screen.blit(pieceObject.sprite, (HEIGHT * 0.9, HEIGHT * 0.7))#bro why is this inverted x should always horizontal
            upgrades = "Upgrades: "
            debuffs = "Debuffs: "
            if (pieceObject.get_isUpgraded()):
                upgrades += pieceObject.get_upgrade_desc()
            else:
                upgrades += "None"
            if (pieceObject.get_isDebuffed()):
                debuffs += pieceObject.get_debuff_desc()
            else:
                debuffs += "None"
            button = TextButton((255,255,255),0,(HEIGHT * 0.8),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,upgrades,None)
            button.hover = False
            button.draw(self.screen)
            button = TextButton((255,255,255),0,(HEIGHT * 0.9),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,debuffs,None)
            button.hover = False
            button.draw(self.screen)

    def draw_grid(self):
        font = pygame.font.Font(None, 25) 
        #if (self.board.mycolor == "white"):
        for i in range (8):
            if self.board.mycolor == "black":
                text_surf = font.render(str(1 + i), True, "black")
                rect = text_surf.get_rect(center=(10, HEIGHT*.1 * i + (HEIGHT*0.015)))
                self.screen.blit(text_surf, rect)

                text_surf = font.render(str(chr(ord("h") - i)), True, "black")
                rect = text_surf.get_rect(center=(WIDTH*.1 * i - 10+ WIDTH*.1,HEIGHT*.8 - 10))
                self.screen.blit(text_surf, rect)
            if self.board.mycolor == "white":
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
        if (self.board.mycolor == "white"):
            #print ("white", len(self.board.whitePieces), " - ", len(self.board.blackPieces))
            for x,y in self.board.whitePieces:
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow, (y * (HEIGHT * 0.1) + 50, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for x,y in self.board.blackPieces:
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, (y *(HEIGHT * 0.1) , x  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow, (y * (HEIGHT * 0.1) + 50, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
        else:
            #print ("black", len(self.board.whitePieces), " - ", len(self.board.blackPieces))
            for i in range(len(self.board.whitePieces)):
                x = self.board.whitePieces[i][0]
                y = self.board.whitePieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow,  ((7-y) * (HEIGHT * 0.1) + 50, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
                    self.screen.blit(downarrow,  ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for i in range(len(self.board.blackPieces)):
                x = self.board.blackPieces[i][0]
                y = self.board.blackPieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, ((7-y) *(HEIGHT * 0.1) , (7-x)  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow,  ((7-y) * (HEIGHT * 0.1) + 50, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
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
            button = TextButton((255,255,255),0,(HEIGHT * 0.8),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,"",None)
            button.hover = False
            button.draw(self.screen)
            button = TextButton((255,255,255),0,(HEIGHT * 0.9),(HEIGHT * 0.8) ,(HEIGHT * 0.1), 15,"",None)
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
        if (self.whitekinginCheck):
            x,y = self.board.getKingLocation("white")
            if (self.board.mycolor == "white"):
                pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            if (self.board.mycolor == "black"):
                pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
        if (self.blackkinginCheck):
            x,y = self.board.getKingLocation("black")
            if (self.board.mycolor == "white"):
                pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            if (self.board.mycolor == "black"):
                pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)

    #promotion callback

    def promote(self, x,y,piece):
        self.board.chessArray[x][y] = None
        if self.board.mycolor =="white":
            self.board.whitePieces.remove((x,y))
        if self.board.mycolor =="black":
            self.board.blackPieces.remove((x,y))
        self.board.addPiece(x,y,piece, self.board.mycolor)
        self.move_data["promote"] = piece
        self.offerpromotion = False
        self.moved = True
        self.execute_instruction()

    def draw_promotion_options(self):
    
        i = self.move_data["x0"]
        j = self.move_data["y0"]

        offset = 10

        font = pygame.font.Font(None, 36) 
        if (self.board.mycolor == "black"):
            options = ["resources/Chess_ndt60.png", "resources/Chess_rdt60.png", "resources/Chess_bdt60.png", "resources/Chess_qdt60.png"]
            n = ["kn", "r", "b", "q"]
            for k in range(2,6):
                piece_background = TextButton((150,150,150),(HEIGHT * 0.85) , (HEIGHT * k * 0.1 + offset * k),(HEIGHT * 0.1),(HEIGHT * 0.1) ,0, "",None)
                piece_background.draw(self.screen)
                piece_promote = ImageButton((HEIGHT * 0.85) , (HEIGHT * k * 0.1 + offset * k),(HEIGHT * 0.1) ,(HEIGHT * 0.1), options[k-2],1, self.promote, i,j,n[k-2])
                piece_promote.draw(self.screen)
        if (self.board.mycolor == "white"):
            options = ["resources/Chess_nlt60.png", "resources/Chess_rlt60.png", "resources/Chess_blt60.png", "resources/Chess_qlt60.png"]
            n = ["kn", "r", "b", "q"]
            for k in range(2,6):
                piece_promote = ImageButton((HEIGHT * 0.8) , (HEIGHT * k * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1), options[k-2],1, self.promote, i,j,n[k-2])
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
                        if (self.board.mycolor == "white"):
                            self.selectsquare(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
                        else:
                            self.selectsquare(7 - event.pos[1] // (WIDTH // 10),7 - event.pos[0] // (WIDTH // 10))

            self.screen.fill((105,146,62))
            self.draw_board()
            self.draw_pieces()
            if self.offermodifiers:
                self.draw_modifiers()
            else:
                self.modifiers = []

            self.draw_grid()
            self.draw_selected_info()
            if not self.offermodifiers and self.offerpromotion:
                self.draw_promotion_options()
            if self.endgame != "":
                color = (105, 194, 250)
                button = TextButton(color,(HEIGHT * 0.2),(HEIGHT * 0.3) ,(HEIGHT * 0.4), (HEIGHT * 0.2),50,self.endgame,None)
                button.hover = False
                button.draw(self.screen)

            #self.draw_promotion_options()
            #print("Offering modifiers is ", self.offermodifiers, " because ", self.turnCount)
            pygame.display.flip()

            #if (self.moved and not(self.offermodifiers)):

            if (self.moved and not(self.offermodifiers)):
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
        host_button = ImageButton(button_x_pos,HEIGHT//2 - height_offset, 57,9, "resources/create_game_button.png",scale, None)
        join_button =  ImageButton(button_x_pos,HEIGHT//2 + height_offset,57,9, "resources/join_game_button.png",scale, None)
        textbox_width = 350
        textbox_height = 50
#for joining game menu
        #TODO:add color pallete globals cuz this shits getting ugly
        ip_textbox = Textbox((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 - height_offset, textbox_width,textbox_height, textbox_height-8, "ip")
        port_textbox = Textbox((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 + height_offset, textbox_width,textbox_height, textbox_height-8, "port")
        connect_button = TextButton((150,150,150), (WIDTH - textbox_width) // 2, HEIGHT//2 + 3*height_offset, textbox_width,textbox_height, textbox_height-8, "join game",None)
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
