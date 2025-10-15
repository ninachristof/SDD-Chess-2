from chesspiece import *
import tkinter as tk
import board

import os #need this for the images if we want to use relative paths?

#colors = ['#a52a2a','#ffffff']
colors = ['#FFDAB9','#008000']

def printout():
    print("hello world")
class game:
    board = None
    turn = None
    currentSquare = None
    newSquare = None
    turn = "white"

    def __init__(self):
        #self.board = [ [None for j in range(8)] for i in range(8)]
        #Initialize Pawns
        # for i in range (8):
        #     self.board[1][i] = pawn(1,i,"black")
        #     self.board[6][i] = pawn(6,i,"white")
        
        # #Initialize Knights
        # self.board[7][1] = knight(7,1,"white")
        # self.board[7][6] = knight(7,6,"white")
        # self.board[0][1] = knight(0,1,"black")
        # self.board[0][6] = knight(0,6,"black")
        
        # # Initialize Rooks
        # self.board[7][0] = rook(7,0,"white")
        # self.board[7][7] = rook(7,7,"white")
        # self.board[0][0] = rook(0,0,"black")
        # self.board[0][7] = rook(0,7,"black")

        # # Initialize Bishops
        # self.board[7][2] = bishop(7,2,"white")
        # self.board[7][5] = bishop(7,5,"white")
        # self.board[0][2] = bishop(0,2,"black")
        # self.board[0][5] = bishop(0,5,"black")
        
        # # Initialize Kings and Queens
        # self.board[7][4] = king(7,2,"white")
        # self.board[7][3] = queen(7,5,"white")
        # self.board[0][4] = king(0,2,"black")
        # self.board[0][3] = queen(0,5,"black")
        self.board = board.board()
        self.board.whitePieceCheck()
        self.board.blackPieceCheck()

        # for i in range(8):
        #     for j in range(8):
        #         if (self.board[i][j] == None):
        #             continue
        #         elif (self.board[i][j].get_name() == 'p'):
        #             self.board.pawnCheck(i,j,'w')


        
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
         
                    
    def selectsquare(self,i,j,root):
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

                self.board.movePiece(i,j,currentX,currentY,self.turn)

                # self.board.chessArray[i][j] = self.board.getSquare(currentX,currentY)
                # self.board.chessArray[currentX][currentY] = None
                # self.currentSquare = None

                if (self.turn == "white"):
                    self.turn = "black"
                else:
                    self.turn = "white"
                
                root.destroy()
                #self.rotateBoard()

                self.board.whitePieceCheck()
                self.board.blackPieceCheck()
                self.currentSquare = None
                self.display()
                
            else: 
                print("Invalid move")
                return


    def display(self):
        root = tk.Tk()
        root.geometry("800x800")
        frm = tk.Frame(root)
        frm.grid()
        

        #print(self.board)
        # #Specify Grid
        # tk.Grid.rowconfigure(root,0,weight=1)
        # tk.Grid.columnconfigure(root,0,weight=1)

        for i in range(10):
            tk.Grid.columnconfigure(root,i,weight=1)
            tk.Grid.rowconfigure(root,i,weight=1)

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
                    # button = tk.Button(root, image = photo)                        #need lambda to pass args for the command function
                    button = tk.Button(root, text = self.board.getSquare(i,j).get_name(), command = lambda a = i, b = j, c = root:self.selectsquare(a,b,c),bg = colors[(i+j)%2],fg = self.board.getSquare(i,j).get_color(), font=("Arial", 16))
                else:
                    button = tk.Button(root, text = "", command = lambda a = i, b = j:self.selectsquare(a,b,root),bg = colors[(i+j)%2])
                newrow.append(button)
                button.grid(row = i,column = j, sticky = "NSEW")
            buttons.append(newrow)

        root.mainloop()     