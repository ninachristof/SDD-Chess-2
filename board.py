from chesspiece import *

class board:
    chessArray = [[None for j in range(8)] for i in range(8)]
    whitePieces = []
    blackPieces = []

    def addPiece(self, x, y, piece, color):
        # The coordinates of this are a little messed up. 
        # Current system: X is vertical going downwards, Y is horizontal going Right.
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print("({0}, {1}) is not a valid coordinate.".format(x, y))
            return
        if (color != "black" and color != "white"):
            print("{} is not a valid color.".format(color))
            return

        if (self.chessArray[x][y] != None):
            print("The {} {} piece cannot be placed at ({}, {}) because there is already a {} {} piece there".format(color, piece, x, y, self.chessArray[x][y].get_color(), self.chessArray[x][y].get_name()))
            return

        if (piece == "p"):
            self.chessArray[x][y] = pawn(x, y, color)
        elif (piece == "kn"):
            self.chessArray[x][y] = knight(x, y, color)
        elif (piece == "r"):
            self.chessArray[x][y] = rook(x, y, color)
        elif (piece == "b"):
            self.chessArray[x][y] = bishop(x, y, color)
        elif (piece == "q"):
            self.chessArray[x][y] = queen(x, y, color)
        elif (piece == "k"):
            self.chessArray[x][y] = king(x, y, color)
        else:
            print("{} is not a valid piece. Try again.".format(piece))
            return

        if (color == "white"):
            self.whitePieces.append((x, y))
        else:
            self.blackPieces.append((x, y))


    def __init__(self): # Initial board setup. 
        # Initialize Pawns
        for i in range(8):
            self.addPiece(1, i, "p", "black")
            self.addPiece(6, i, "p", "white")

        # Initialize Knights
        self.addPiece(7, 1, "kn", "white")
        self.addPiece(7, 6, "kn", "white")
        self.addPiece(0, 1, "kn", "black")
        self.addPiece(0, 6, "kn", "black")

        
        # Initialize Rooks
        self.addPiece(7, 0, "r", "white")
        self.addPiece(7, 7, "r", "white")
        self.addPiece(0, 0, "r", "black")
        self.addPiece(0, 7, "r", "black")

        # Initialize Bishops
        self.addPiece(7, 2, "b", "white")
        self.addPiece(7, 5, "b", "white")
        self.addPiece(0, 2, "b", "black")
        self.addPiece(0, 5, "b", "black")
        
        # Initialize Kings and Queens
        self.addPiece(7, 4, "k", "white")
        self.addPiece(7, 3, "q", "white")
        self.addPiece(0, 4, "k", "black")
        self.addPiece(0, 3, "q", "black")

        # self.addPiece(0, 3, "k", "white")

    def clear(self):
        self.chessArray = [[None for j in range(8)] for i in range(8)]
        self.whitePieces = []
        self.blackPieces = []

    def PawnState(self):
        self.clear()
        self.addPiece(0, 1, "p", "white")
        self.addPiece(5, 2, "p", "white")
        self.chessArray[5][2].set_first_move()
        self.addPiece(6, 4, "p", "white")
        self.addPiece(6, 6,"p", "white")
        self.addPiece(2, 5,"p", "white")
        self.addPiece(6, 1,"p", "white")

        self.addPiece(4, 3, "p", "black")
        self.addPiece(1, 5, "p", "black")
        self.addPiece(4, 6, "p", "black")
        self.addPiece(5, 0, "p", "black")


    def printBoardState(self):
        print("  ", end="") 
        for i in range(8):
            print("|  {} ".format(i), end="")
        print("|")
        print("-" * 41)
        for i in range(8):
            print("{} |".format(i), end="")
            for j in range(8):
                if (self.chessArray[i][j] != None):
                    print("{0:4}".format(self.chessArray[i][j].get_name() + " " + self.chessArray[i][j].get_color()[0]), end="|")
                else:
                    print("   ", end=" |")
            print("\n  " + "-" * 41)
    
    def rookCheck(self):
        return
    
    def knightCheck(self, x, y):
        return

    # def pawnCheck(self, x, y, color): # Inputs: The X and Y of a pawn piece on the board. 

    #     return

    def whitePieceCheck(self):
        for x, y in self.whitePieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                # Forwards movement
                if (x != 0 and self.chessArray[x - 1][y] == None):
                    possibleMoves.append((x - 1, y))
                    if (x != 1 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x - 2][y] == None):
                        possibleMoves.append((x - 2, y))
                
                # Capture Movement
                if (x != 0 and y != 0 and self.chessArray[x - 1][y - 1] != None and (not self.chessArray[x - 1][y - 1].isWhite())):
                    possibleMoves.append((x - 1, y - 1))
                if (x != 0 and y != 7 and self.chessArray[x - 1][y + 1] != None and (not self.chessArray[x - 1][y + 1].isWhite())):
                    possibleMoves.append((x - 1, y + 1))
            elif (self.chessArray[x][y].get_name() == "r"):
                self.rookCheck()
            # print(self.chessArray[x][y].get_name() + " " + self.chessArray[x][y].get_color()[0] + " {0}, {1}".format(x, y))
            print("WHITE {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)

    def blackPieceCheck(self):
        for x, y in self.blackPieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                # Forwards movement
                if (x != 7 and self.chessArray[x + 1][y] == None):
                    possibleMoves.append((x + 1, y))
                    if (x != 6 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x + 2][y] == None):
                        possibleMoves.append((x + 2, y))
                
                # Capture Movement
                if (x != 7 and y != 0 and self.chessArray[x + 1][y - 1] != None and (self.chessArray[x + 1][y - 1].isWhite())):
                    possibleMoves.append((x + 1, y - 1))
                if (x != 7 and y != 7 and self.chessArray[x + 1][y + 1] != None and (self.chessArray[x + 1][y + 1].isWhite())):
                    possibleMoves.append((x + 1, y + 1))
            print("BLACK {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)

'''
EN PASSANT CHECK: 
    Capturing en passant is permitted only on the turn *immediately* 
    after the two-square advance; it cannot be done on a later turn. 
This means that a pawn needs a boolean or something so it knows it moved twice.
'''

def main():
    newgame = board()
    newgame.PawnState()
    newgame.printBoardState()
    newgame.whitePieceCheck()
    newgame.blackPieceCheck()
main()