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
                self.new_p2p.sendInstruction(self.current_instruction)
                global_vars.send_event.clear()
                wait_for_my_move = False
            else:
                #wait for instruction
                instruction = self.new_p2p.recvInstruction() 
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    break
                self.execute_instruction(instruction[0],instruction[1],instruction[2],instruction[3])
                wait_for_my_move = True
        #self.new_p2p.close_all()


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

    def setup_game(self):
        if(self.conn_type == "connect"):
            self.board.mycolor = "black"
            
        else:
            self.board.mycolor = "white"
        #self.board.startState()
        #self.board.whitePieceUpdateLegal()
        #elf.board.blackPieceUpdateLegal()

    def get_conn_thread(self):
        return self.conn_thread
        
    def execute_instruction(self,i,j,currentX,currentY):
        #print("Moving a piece from ", i , ", ", j , " to ", currentX, ", ", currentY)
        self.clickedSquare = None
        self.board.movePiece(i,j,currentX,currentY,self.turn)

        if (self.turn == "black"):
            self.turnCount += 1
        
        whiteMoves = self.board.updateLegal("white")
        blackMoves = self.board.updateLegal("black")

        if (whiteMoves == 0):
            if (self.board.isKinginCheck("white")):
                print("Checkmate! Black Wins")
            else:
                print("Stalemate! White has no valid moves")
        if (blackMoves == 0):
            if (self.board.isKinginCheck("black")):
                print("Checkmate! White Wins")
            else:
                print("Stalemate! Black has no valid moves")
        self.currentSquare = None

        print ("The white king is at ", self.board.getKingLocation("white"))
        print ("The black king is at ", self.board.getKingLocation("black"))
        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"

    def selectsquare(self,i,j):
        if (self.board.getSquare(i,j) != None):
            self.clickedSquare = (i,j)
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

                #debugging
                pieceObject = self.board.chessArray[i][j]
                #print("Possible moves are")
                print(self.board.getPossibleMoves(i,j,pieceObject.color))
                #print("Legal moves are ")
                print(pieceObject.getlegalMoves())
                return
        
        #At this point, you have already selected a piece
        #If you selected another of your piece, swap the current piece to it
        elif (not(self.board.getSquare(i,j) == None) and self.board.getSquare(i,j).get_color() == self.turn):
            #print("Selected a piece at ", i , "," , j)
            self.currentSquare = (i,j)
            # print(self.board.chessArray[i][j].get_name())
            # print(self.board.chessArray[i][j].upgrades)
            # print(self.board.chessArray[i][j].get_possible_moves())

            pieceObject = self.board.chessArray[i][j]
            #print("Possible moves are")
            print(self.board.getPossibleMoves(i,j,pieceObject.color))
            #print("Legal moves are ")
            print(pieceObject.getlegalMoves())
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
                self.current_instruction = struct.pack("iiii5s",i, j, currentX, currentY, bytes(self.board.mycolor,"utf-8"))
                self.moved = True
                self.execute_instruction(i,j,currentX,currentY)

                if (self.turnCount > 0 and (self.turnCount % 2 == 0)):
                    self.offermodifiers = True
                else:
                    self.offermodifiers = False

                # while (self.offermodifiers):
                #     print("Waiting for user to use a powerup")

                #global_vars.send_event.set()
            else: 
                #print("Invalid move")
                return

    def draw_modifiers(self):
        #print(self.offermodifiers, " because ", self.turnCount)
        if (not(self.offermodifiers)):
            return
        red = (255,0,0)

        if (len(self.modifiers) == 0):
            pieces = self.board.whitePieces + self.board.blackPieces
            # if (self.board.mycolor == "black"):
            #     my_pieces = self.board.blackPieces
            for piece in pieces:
                if (self.board.chessArray[piece[0]][piece[1]].get_name() == "k"):
                    pieces.remove(piece)
            for i in range(4):
                randomPiece = pieces[rand.randint(0,len(pieces)-1)]
                if (self.board.chessArray[randomPiece[0]][randomPiece[1]].get_color() == self.board.mycolor):
                    powerup = modifiers.getPowerups(self.board.chessArray[randomPiece[0]][randomPiece[1]].get_name())
                    powerupdescription = "Your " + self.board.chessArray[randomPiece[0]][randomPiece[1]].get_name() + " at " + str(randomPiece) + powerup.get_description()
                    print("Power up ", i, " - " , powerupdescription)
                    self.modifiers.append((randomPiece,powerup,powerupdescription))
                else:
                    debuff = modifiers.getDebuff()
                    debuffdescription = "Your opponent's " + self.board.chessArray[randomPiece[0]][randomPiece[1]].get_name() + " at " + str(randomPiece) + debuff.get_description()
                    print("Debuff ", i, " - " , debuffdescription)
                    self.modifiers.append((randomPiece,debuff,debuffdescription))
        for i in range(2,6):
            randomPiece,modifier,description = self.modifiers[i-2]
            button = TextButton((250,50,50), (HEIGHT * 0.8) , (HEIGHT * i * 0.1),(HEIGHT * 0.2) ,(HEIGHT * 0.1), 15, description ,None)
            button.draw(self.screen)
        for i in range(2,7):
            pygame.draw.line(self.screen, 'black', (HEIGHT*0.8,(HEIGHT * 0.1)  * i), ((HEIGHT),(HEIGHT * 0.1) * i), 2)

    def draw_valid(self):
        if(self.clickedSquare != None):
            currentX, currentY = self.clickedSquare
            #print("Drawing valid for ", currentX, ",", currentY)
            pieceObject = self.board.getSquare(currentX,currentY)
            #print("got object at ", currentX, ",", currentY)
            validMoves = pieceObject.getlegalMoves()
            #print("Drawing validMoves for ", currentX, ",", currentY)
            gray = (100, 100, 100)     # darker gray
            green = (30, 60, 10)
            blue = (0,0,255)
            #print("Possible moves are")
            #print(self.board.getPossibleMoves(currentX,currentY,pieceObject.get_color()))
            #print("Valid moves are ")
            #print(validMoves)
            for move in validMoves:
                #print("Move is ", move)
                adj_mov = ((8 * move[0]) + move[1])
                if (self.board.mycolor == "white"):
                    #surface,color,center coords, radius, optional width (0 fills the circle)
                    pygame.draw.circle(self.screen,blue,[((move[1] * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),move[0] * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                    # if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                    #     pygame.draw.rect(self.screen, gray, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                    # else:
                    #     pygame.draw.rect(self.screen, green, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                if (self.board.mycolor == "black"):
                    pygame.draw.circle(self.screen,blue,[(((7-move[1]) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-move[0]) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                    # if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                    #     pygame.draw.rect(self.screen, gray, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7-move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                    # else:
                    #     pygame.draw.rect(self.screen, green, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7 - move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])

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
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1) + 10, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for x,y in self.board.blackPieces:
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, (y *(HEIGHT * 0.1) , x  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow, (y * (HEIGHT * 0.1) + 50, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
                    self.screen.blit(downarrow, (y * (HEIGHT * 0.1) + 10, x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
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
                    self.screen.blit(downarrow,  ((7-y) * (HEIGHT * 0.1) + 10, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for i in range(len(self.board.blackPieces)):
                x = self.board.blackPieces[i][0]
                y = self.board.blackPieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, ((7-y) *(HEIGHT * 0.1) , (7-x)  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
                if (piece.get_isUpgraded()):
                    self.screen.blit(uparrow,  ((7-y) * (HEIGHT * 0.1) + 50, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
                if (piece.get_isDebuffed()):
                    self.screen.blit(downarrow,  ((7-y) * (HEIGHT * 0.1) + 10, (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal

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
                pygame.draw.rect(self.screen, 'black', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)])
                pygame.draw.rect(self.screen, 'gray', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)], 5)
                pygame.draw.rect(self.screen, 'gold', [(HEIGHT * 0.8), 0, (HEIGHT * 0.8), (HEIGHT * 0.8)], 5)
                status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                            'Black: Select a Piece to Move!', 'Black: Select a Destination!']
                self.draw_valid()
                for i in range(9):
                    pygame.draw.line(self.screen, 'black', (0,(HEIGHT * 0.1)  * i), ((HEIGHT * 0.8),(HEIGHT * 0.1) * i), 2)
                    pygame.draw.line(self.screen, 'black', ((HEIGHT * 0.1)* i, 0), ((HEIGHT * 0.1)* i, (HEIGHT * 0.8)), 2)
            red = (255,0,0)
            if (self.board.isKinginCheck("white")):
                x,y = self.board.getKingLocation("white")
                if (self.board.mycolor == "white"):
                    pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                if (self.board.mycolor == "black"):
                    pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
            if (self.board.isKinginCheck("black")):
                x,y = self.board.getKingLocation("black")
                if (self.board.mycolor == "white"):
                    pygame.draw.circle(self.screen,red,[((y * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),x * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)
                if (self.board.mycolor == "black"):
                    pygame.draw.circle(self.screen,red,[(((7-y) * (HEIGHT * 0.1)) + (HEIGHT * 0.1)/2),(7-x) * (HEIGHT * 0.1) +  (HEIGHT * 0.1)/2],30)

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (event.pos[0] < 0.8 * WIDTH):
                        if (self.board.mycolor == "white"):
                            self.selectsquare(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
                        else:
                            self.selectsquare(7 - event.pos[1] // (WIDTH // 10),7 - event.pos[0] // (WIDTH // 10))
                    if (event.pos[0] >= 0.8 * WIDTH and event.pos[1] >= (HEIGHT * 0.2)
                        and event.pos[1] <= (HEIGHT * 0.6) and self.offermodifiers):
                        #print("Chose powerup ", (event.pos[1] - HEIGHT * 0.2) // (WIDTH // 10))
                        randomPiece, powerup,description = self.modifiers[int(event.pos[1] - HEIGHT * 0.2) // (WIDTH // 10)]
                        print(self.board.chessArray[randomPiece[0]][randomPiece[1]].get_name(), " at ", randomPiece[0], ",", randomPiece[1], " is getting modified")
                        # print(powerup.get_capture())
                        # print(powerup.get_move())
                        if (self.board.chessArray[randomPiece[0]][randomPiece[1]].get_color() == self.board.mycolor):
                            self.board.chessArray[randomPiece[0]][randomPiece[1]].upgrades = [powerup.get_capture(),powerup.get_move()]
                        else:
                            print("debuffing opponent's piece!")
                        self.offermodifiers = False
                        self.modifiers = []
                    # elif (event.pos[0] == 0.8 * WIDTH):
                    #     self.offermodifiers = False
            self.screen.fill((105,146,62))
            self.draw_board()
            self.draw_pieces()
            self.draw_modifiers()
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
        host_button = ImageButton(button_x_pos,HEIGHT//2 - height_offset, None,"resources/create_game_button.png",57,9,scale)
        join_button =  ImageButton(button_x_pos,HEIGHT//2 + height_offset, None,"resources/join_game_button.png",57,9,scale)
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
