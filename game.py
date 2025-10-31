from chesspiece import *
import threading
import board
import struct
from p2p import *
import global_vars
import pygame

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
    mycolor = "white"
    conn_thread = None
    new_p2p = None
    screen = None
    current_instruction = ""
    running = True

#running this function on a separte thread
    def run_socket(self,conn_type, ip, port):
        self.new_p2p = p2p(conn_type, ip, port)
        self.new_p2p.init_p2p()
        wait_for_my_move = True
        if(conn_type == "connect"):
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
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    break
                self.execute_instruction(instruction[0], instruction[1],instruction[2],instruction[3])
                wait_for_my_move = True
        self.new_p2p.close_all()

    def __init__(self, conn_type, ip, port):
        self.board = board.board()
        self.board.startState()
        self.board.whitePieceUpdate()
        self.board.blackPieceUpdate()
        if(conn_type == "connect"):
            self.mycolor = "black"
        self.conn_thread = threading.Thread(target=self.run_socket, args=(conn_type, ip, port))
        self.conn_thread.start()
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(f"Chess {self.mycolor}")
        #TODO:somwhere to join or force join this thread
        
    def get_conn_thread(self):
        return self.conn_thread
        
    def rotateBoard(self):
        print("Rotating board")
        # Create a new baord to initialize values into 
        newBoard = [[None for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8): 
                # Find new x and y positions
                newX = abs(x - 7)
                newY = abs(y - 7)
                #print(f"Old  x {x} new x {newX} old y {y} new y {newY}")
                newBoard[newX][newY] = self.board[x][y]
                
        # Set board to new board
        self.board = newBoard
         
                    
    def execute_instruction(self,i,j,currentX,currentY):
        self.board.movePiece(i,j,currentX,currentY,self.turn)

        if (self.turn == "white"):
            self.turn = "black"
        else:
            self.turn = "white"
        
        self.board.whitePieceUpdate()
        self.board.blackPieceUpdate()
        self.currentSquare = None

    def selectsquare(self,i,j):
        print("SELECT SQUARE")
        print(self.board.whitePieces)
        print(self.board.blackPieces)
        if(self.turn != self.mycolor):
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
            validMoves = pieceObject.get_possible_moves()
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
                self.current_instruction = struct.pack("iiii5s",i, j, currentX, currentY, bytes(self.mycolor,"utf-8"))

                global_vars.send_event.set()
                self.execute_instruction(i,j,currentX,currentY)
                
            else: 
                print("Invalid move")
                return

    def draw_valid(self):
        if(self.currentSquare != None):
            currentX, currentY = self.currentSquare
            pieceObject = self.board.getSquare(currentX,currentY)
            validMoves = pieceObject.get_possible_moves()
            gray = (180,180,180)
            green = (55,96,12)
            for move in validMoves:
                adj_mov = ((8 * move[0]) + move[1])
                if (((8 * move[0]) + (move[1] )) + (move[0] % 2)) % 2 == 0:
                    pygame.draw.rect(self.screen, gray, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])
                else:
                    pygame.draw.rect(self.screen, green, [ (move[1] * (HEIGHT * 0.1) ), move[0] * (HEIGHT * 0.1),(HEIGHT * 0.1) ,(HEIGHT * 0.1) ])

    def draw_captured(self):
        pass
    def draw_pieces(self):
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

    def draw_board(self):
        for i in range(32):
            column = i % 4
            row = i // 4
            color = (255,255,255)
            if row % 2 == 0:
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

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False#TODO: THIS SHIT NOT WORKING
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.selectsquare(event.pos[1] // (WIDTH // 10), event.pos[0] // (WIDTH // 10))
            self.screen.fill((105,146,62))
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            #self.draw_captured()

        pygame.display.quit()
        pygame.quit()
        global_vars.send_event.set()
