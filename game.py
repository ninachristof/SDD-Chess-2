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
        self.board = board.board()
        
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
                print("Selected one of your pieces at ", i , "," , j)
                self.currentSquare = (i,j)
                print("The possible moves for this piece are ", self.board.getLegalMoves(i,j))
                return
        
        #At this point, you have already selected a piece
        #If you selected another of your piece, swap the current piece to it
        elif (not(self.board.getSquare(i,j) == None) and self.board.getSquare(i,j).get_color() == self.turn):
            print("Selected a piece at ", i , "," , j)
            self.currentSquare = (i,j)
            print("The possible moves for this piece are ", self.board.getLegalMoves(i,j))
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

                self.board.whitePieceUpdateLegal()
                self.board.blackPieceUpdateLegal()
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
                    #need lambda to pass args for the command function
                    button = tk.Button(root, text = self.board.getSquare(i,j).get_name(),
                                        command = lambda a = i, b = j, c = root:self.selectsquare(a,b,c),
                                        bg = colors[(i+j)%2],fg = self.board.getSquare(i,j).get_color(),
                                        font=("Arial", 16))
                else:
                    button = tk.Button(root, text = "", command = lambda a = i, 
                                       b = j:self.selectsquare(a,b,root),bg = colors[(i+j)%2])
                newrow.append(button)
                button.grid(row = i,column = j, sticky = "NSEW")
            buttons.append(newrow)

        root.mainloop()     