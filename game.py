from chesspiece import *
import threading
import board
import struct
from p2p import *
import global_vars
import pygame
from state import *
from textbox import *
from button import *
from colors import *
from utils import *
import time

import os #need this for the images if we want to use relative paths?


#colors = ['#a52a2a','#ffffff']
colors = ['#FFDAB9','#008000']
WIDTH = 800
HEIGHT = 800


def printout():
    print("hello world")


class game:
    #root = None
    board = None
    turn = None
    currentSquare = None
    newSquare = None
    turn = "white"
    conn_thread = None
    new_p2p = None
    screen = None
    current_instruction = ""
    running = True
    ip = ""
    port = 0
    conn_type = ""

#running this function on a separte thread

    def __init__(self, conn_type, ip, port):
        self.conn_type = conn_type
        self.ip = ip
        self.port = port
        self.board = board.board()
        self.conn_thread = threading.Thread(target=self.run_socket)
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(f"Chess {self.board.mycolor}")
        #TODO:somwhere to join or force join this thread

    def setup_game(self):
        if(self.conn_type == "connect"):
            self.board.mycolor = "black"
        else:
            self.board.mycolor = "white"
        self.board.startState(self.board.mycolor)
        self.board.whitePieceUpdateLegal()
        self.board.blackPieceUpdateLegal()
        
    def run_socket(self):
        print("RUNNING SOCKET")
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
                self.new_p2p.send_instruction_2(self.current_instruction)
                global_vars.send_event.clear()
                wait_for_my_move = False
            else:
                #wait for instruction
                instruction = self.new_p2p.recv_instruction_2() 
                print(f"{instruction[0]}, {instruction[0]}")
                print(f"{instruction[2]}, {instruction[2]}")
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    break
                self.execute_instruction(instruction[0],instruction[1],instruction[2],instruction[3])
                wait_for_my_move = True
        self.new_p2p.close_all()

    def get_conn_thread(self):
        return self.conn_thread
                    
    def execute_instruction(self,i,j,currentX,currentY):
        print("Moving a piece from ", i , ", ", j , " to ", currentX, ", ", currentY)
        self.board.movePiece(i,j,currentX,currentY,self.turn)

        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"
        
        whiteMoves = self.board.whitePieceUpdateLegal()
        blackMoves = self.board.blackPieceUpdateLegal()
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

    def selectsquare(self,i,j):
        print("SELECT SQUARE")
        print(self.board.whitePieces)
        print(self.board.blackPieces)
        if(self.turn != self.board.mycolor):
            return
        print("selected square ", i , "," , j)

        if (self.currentSquare == None):
            if (self.board.getSquare(i,j) == None or not(self.board.getSquare(i,j).get_color() == self.turn)):
                print("Invalid square")
                return
            else: #The square you selected must be one of your pieces
                print("Selected a piece at ", i , "," , j)
                self.currentSquare = (i,j)
                return
        
        #At this point, you have already selected a piece
        #If you selected another of your piece, swap the current piece to it
        elif (not(self.board.getSquare(i,j) == None) and self.board.getSquare(i,j).get_color() == self.turn):
            print("Selected a piece at ", i , "," , j)
            self.currentSquare = (i,j)
            return
        
        #Otherwise, you are attempting to make a move; see if this move is possible, and do it if so
        else:
            currentX, currentY = self.currentSquare
            newX, newY = i, j
            pieceObject = self.board.getSquare(currentX,currentY)
            pieceName = pieceObject.get_name()
            validMoves = self.board.getLegalMoves(currentX,currentY)
            pieceObject.set_first_move()
            pieceColor = pieceObject.get_color()
            wantedMoveXY = (newX,newY)
            print(f"Moving a {pieceColor} {pieceName} from {currentX}, {currentY} to {newX}, {newY}")
            print(f"Possible moves {validMoves} wanted moves {wantedMoveXY}")
            
            # Check if it is a valid move
            if (validMoves == None):
                print("Invalid move")
                return
            if wantedMoveXY in validMoves:
                print("Valid Move")
                self.current_instruction = struct.pack("iiii5s",i, j, currentX, currentY, bytes(self.board.mycolor,"utf-8"))

                global_vars.send_event.set()
                self.execute_instruction(i,j,currentX,currentY)
                
            else: 
                print("Invalid move")
                return

    def draw_valid(self):
        if(self.currentSquare != None):
            currentX, currentY = self.currentSquare
            pieceObject = self.board.getSquare(currentX,currentY)
            validMoves = self.board.getLegalMoves(currentX,currentY)
            for move in validMoves:
                print("Move is ", move)
                adj_mov = ((8 * move[0]) + move[1])
                if (self.board.mycolor == "white"):
                    if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                        pygame.draw.rect(self.screen, c.SELECT_GRAY, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                    else:
                        pygame.draw.rect(self.screen, c.SELECT_GREEN, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                if (self.board.mycolor == "black"):
                    if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                        pygame.draw.rect(self.screen, c.SELECT_GRAY, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7-move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                    else:
                        pygame.draw.rect(self.screen, c.SELECT_GREEN, [ ((7-move[1]) * (HEIGHT * 0.1) ), (7 - move[0]) * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])

    def draw_captured(self):
        pass
    def draw_pieces(self):
        if (self.board.mycolor == "white"):
            for i in range(len(self.board.whitePieces)):
                x = self.board.whitePieces[i][0]
                y = self.board.whitePieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, (y * (HEIGHT * 0.1), x  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for i in range(len(self.board.blackPieces)):
                x = self.board.blackPieces[i][0]
                y = self.board.blackPieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, (y *(HEIGHT * 0.1) , x  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal
        else:
            for i in range(len(self.board.whitePieces)):
                x = self.board.whitePieces[i][0]
                y = self.board.whitePieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, ((7-y) * (HEIGHT * 0.1), (7-x)  * (HEIGHT * 0.1)))#bro why is this inverted x should always horizontal
            for i in range(len(self.board.blackPieces)):
                x = self.board.blackPieces[i][0]
                y = self.board.blackPieces[i][1]
                piece = self.board.chessArray[x][y]
                self.screen.blit(piece.sprite, ((7-y) *(HEIGHT * 0.1) , (7-x)  *(HEIGHT * 0.1) ))#bro why is this inverted x should always horizontal


    def draw_board(self):
            for i in range(32):
                column = i % 4
                row = i // 4
                if row % 2 == 0:
                    pygame.draw.rect(self.screen, c.WHITE, [ (HEIGHT * 0.6) - (column * (HEIGHT * 0.2) ), row * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                else:
                    pygame.draw.rect(self.screen, c.WHITE, [ (HEIGHT * 0.7) - (column * (HEIGHT * 0.2)), row *(HEIGHT * 0.1) ,(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                pygame.draw.rect(self.screen, 'black', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)])
                pygame.draw.rect(self.screen, 'gray', [0, (HEIGHT * 0.8), WIDTH, (HEIGHT * 0.2)], 5)
                pygame.draw.rect(self.screen, 'gold', [(HEIGHT * 0.8), 0, (HEIGHT * 0.8), (HEIGHT * 0.8)], 5)
                status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                            'Black: Select a Piece to Move!', 'Black: Select a Destination!']
                self.draw_valid()
                for i in range(9):
                    pygame.draw.line(self.screen, 'black', (0,(HEIGHT * 0.1)  * i), ((HEIGHT * 0.8),(HEIGHT * 0.1) * i), 2)
                    pygame.draw.line(self.screen, 'black', ((HEIGHT * 0.1)* i, 0), ((HEIGHT * 0.1)* i, (HEIGHT * 0.8)), 2)

    def OLD_main_loop(self):
        self.setup_game()
        self.conn_thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False#TODO: THIS SHIT NOT WORKING
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if (self.board.mycolor == "white"):
                        self.selectsquare(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
                    else:
                        self.selectsquare(7 - event.pos[1] // (WIDTH // 10),7 - event.pos[0] // (WIDTH // 10))
            self.screen.fill(g.BOARD_GREEN)
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            #self.draw_captured()

        pygame.display.quit()
        pygame.quit()
        global_vars.send_event.set()

    def main_loop(self):
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
        ip_textbox = Textbox(c.GRAY_1, (WIDTH - textbox_width) // 2, HEIGHT//2 - height_offset, textbox_width,textbox_height, textbox_height-8, "ip")
        port_textbox = Textbox(c.GRAY_1, (WIDTH - textbox_width) // 2, HEIGHT//2 + height_offset, textbox_width,textbox_height, textbox_height-8, "port")
        connect_button = TextButton(c.LIGHT_BLUE_2, (WIDTH - textbox_width + 100) // 2, HEIGHT//2 + 3*height_offset, textbox_width - 100,textbox_height, textbox_height-8, "   join game for me please",None)
        while self.running:
            eventlist = pygame.event.get()
            #if quit is recieved do so immediately
            for event in eventlist:
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

            if state == "main menu":
                self.screen.fill((172,200,255))
                if host_button.draw(self.screen) == 1:
                    state = "host game"
                if join_button.draw(self.screen) == 1:
                    state = "join game"

            elif state == "host game":
                #time.sleep(1)
                self.conn_type = "host"
                self.ip = "0.0.0.0"
                self.port = 2020 #TODO: display a selected available port
                state = "play game"
                self.setup_game()
                self.conn_thread.start()

            elif state == "join game":
                self.conn_type = "connect"
                self.screen.fill(c.LIGHT_BLUE_1)
                ip = ip_textbox.handle_textbox(self.screen, eventlist)
                port = port_textbox.handle_textbox(self.screen, eventlist)

                #TODO:ename the button draw funciton 
                if(connect_button.draw(self.screen) == 1):
                    if is_num(port) and is_valid_ip(ip):
                        self.port = int(port)
                        state = "play game"
                        self.setup_game()
                        self.conn_thread.start()
                    else:
                        print(f"{ip} {port}")


            elif state == "play game":
                for event in eventlist:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                        if (self.board.mycolor == "white"):
                            self.selectsquare(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
                        else:
                            self.selectsquare(7 - event.pos[1] // (WIDTH // 10),7 - event.pos[0] // (WIDTH // 10))
                self.screen.fill(c.BOARD_GREEN)
                self.draw_board()
                self.draw_pieces()
                
            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        global_vars.send_event.set()
