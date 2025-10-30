from chesspiece import *
import threading
import tkinter as tk
import board
import struct
from p2p import *
import global_vars

import os #need this for the images if we want to use relative paths?


#colors = ['#a52a2a','#ffffff']
colors = ['#FFDAB9','#008000']

def printout():
    print("hello world")
class game:
    root = None
    board = None
    turn = None
    currentSquare = None
    newSquare = None
    turn = "white"
    mycolor = "white"
    conn_thread = None
    new_p2p = None


    def run_socket(self,conn_type, ip, port):
        self.new_p2p = p2p(conn_type, ip, port)
        self.new_p2p.init_p2p()
        wait_for_my_move = True
        if(conn_type == "connect"):
            wait_for_my_move = False

        while(1):
            if(wait_for_my_move):
                global_vars.send_event.wait()
                
                print("done waiting")
                self.new_p2p.send_instruction_2()
                global_vars.send_event.clear()
                wait_for_my_move = False
            else:
                instruction = self.new_p2p.recv_instruction_2() 
                print(f"RECEIVED INSTRUCTION BY {self.mycolor} : {instruction}")
                if(instruction == 1):
                    print("INSTRUCTION ERROR")
                    continue
                #TODO: takeout color
                self.board.movePiece(instruction[0], instruction[1],instruction[2],instruction[3],(instruction[4]).decode("utf-8"))
                #add lock to this or is this probably fine?
                if (self.turn == "white"):
                    self.turn = "black"
                else:
                    self.turn = "white"
                
                #self.root.destroy()
                #self.rotateBoard()

                self.board.whitePieceUpdate()
                self.board.blackPieceUpdate()
                self.currentSquare = None
                #self.display()
                wait_for_my_move = True

    def __init__(self, conn_type, ip, port):
        self.board = board.board()
        self.board.startState()
        self.board.whitePieceUpdate()
        self.board.blackPieceUpdate()
        if(conn_type == "connect"):
            self.mycolor = "black"
        self.conn_thread = threading.Thread(target=self.run_socket, args=(conn_type, ip, port))
        self.conn_thread.start()
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
                pass
                # Move the piece if it is valid
                # self.board[i][j] = self.board[currentX][currentY]
                # self.board[currentX][currentY] = None
                # self.currentSquare = None

                global_vars.current_instruction = struct.pack("iiii5s",i, j, currentX, currentY, bytes(self.mycolor,"utf-8"))

                global_vars.send_event.set()
                self.board.movePiece(i,j,currentX,currentY,self.turn)

                # self.board.chessArray[i][j] = self.board.getSquare(currentX,currentY)
                # self.board.chessArray[currentX][currentY] = None
                # self.currentSquare = None

                if (self.turn == "white"):
                    self.turn = "black"
                else:
                    self.turn = "white"
                
                self.root.destroy()
                #self.rotateBoard()

                self.board.whitePieceUpdate()
                self.board.blackPieceUpdate()
                self.currentSquare = None
                self.display()
                
            else: 
                print("Invalid move")
                return


    def display(self):
        self.root = tk.Tk()
        self.root.geometry("800x800")
        self.root.title(self.mycolor)
        frm = tk.Frame(self.root)
        frm.grid()
        

        #print(self.board)
        # #Specify Grid
        # tk.Grid.rowconfigure(self.root,0,weight=1)
        # tk.Grid.columnconfigure(self.root,0,weight=1)

        for i in range(10):
            tk.Grid.columnconfigure(self.root,i,weight=1)
            tk.Grid.rowconfigure(self.root,i,weight=1)

        buttons = []
        for i in range(8):
            newrow = []
            for j in range(8):
                button = None
                if (self.board.getSquare(i,j) != None):
                    #Attempt at PNGs, they don't work too well D:
                    # base_path = os.path.dirname(__file__)
                    # img_path = os.path.join(base_path,self.board[i][j].image)
                    # photo = tk.PhotoImage(file = img_path)
                    # photo = photo.subsample(50,50) 
                    # button = tk.Button(self.root, image = photo)                        #need lambda to pass args for the command function
                    button = tk.Button(self.root, text = self.board.getSquare(i,j).get_name(), command = lambda a = i, b = j:self.selectsquare(a,b),bg = colors[(i+j)%2],fg = self.board.getSquare(i,j).get_color(), font=("Arial", 16))
                else:
                    button = tk.Button(self.root, text = "", command = lambda a = i, b = j:self.selectsquare(a,b),bg = colors[(i+j)%2])
                newrow.append(button)
                button.grid(row = i,column = j, sticky = "NSEW")
            buttons.append(newrow)

        self.root.mainloop()     
