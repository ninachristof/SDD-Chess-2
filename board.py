from chesspiece import *

class board:
    chessArray = [[None for j in range(8)] for i in range(8)]
    whitePieces = []
    blackPieces = []
    whiteKingCheck = False # Is the white king in check? Should be reset each turn. 
    blackKingCheck = False # Is the black king in check? 

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

    def printBoardState(self):
        print("  ", end="") 
        for i in range(8):
            print("|  {} ".format(i), end="")
        print("|")
        print("-" * 43)
        for i in range(8):
            print("{} |".format(i), end="")
            for j in range(8):
                if (self.chessArray[i][j] != None):
                    print("{0:4}".format(self.chessArray[i][j].get_name() + " " + self.chessArray[i][j].get_color()[0]), end="|")
                else:
                    print("   ", end=" |")
            print("\n  " + "-" * 41)
    
    def rookCheck(self, x, y, color): # The <color> piece at x, y moves orthogonally. 
        possibleMoves = []
        iter = x - 1
        # Check move upwards (x - 1)
        while (iter >= 0 and (self.chessArray[iter][y] == None)):
            possibleMoves.append((iter, y))
            iter -= 1
        if (iter != -1 and self.chessArray[iter][y].get_color() != color):
            possibleMoves.append((iter, y))
            if (self.chessArray[iter][y].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        iter = y + 1
        # Check move right (y + 1)
        while (iter <= 7 and (self.chessArray[x][iter] == None)):
            possibleMoves.append((x, iter))
            iter += 1
        if (iter != 8 and self.chessArray[x][iter].get_color() != color):
            possibleMoves.append((x, iter))
            if (self.chessArray[x][iter].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        iter = x + 1
        # Check move downwards (x + 1)
        while (iter <= 7 and (self.chessArray[iter][y] == None)):
            possibleMoves.append((iter, y))
            iter += 1
        if (iter != 8 and self.chessArray[iter][y].get_color() != color):
            possibleMoves.append((iter, y))
            if (self.chessArray[iter][y].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")
        
        iter = y - 1
        # Check move left (y - 1)
        while (iter >= 0 and (self.chessArray[x][iter] == None)):
            possibleMoves.append((x, iter))
            iter -= 1
        if (iter != -1 and self.chessArray[x][iter].get_color() != color):
            possibleMoves.append((x, iter))
            if (self.chessArray[x][iter].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        return possibleMoves
    
    def bishopCheck(self, x, y, color): # The <color> piece at x, y moves diagonally. 
        possibleMoves = []
        iter = x - 1
        iter2 = y + 1
        # Check move up-right (x - 1, y + 1)
        while (iter >= 0 and iter2 <= 7 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter -= 1
            iter2 += 1
        if (iter != -1 and iter2 != 8 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))
            if (self.chessArray[iter][iter2].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        iter = x + 1
        iter2 = y + 1
        # Check move down-right (x + 1, y + 1)
        while (iter <= 7 and iter2 <= 7 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter += 1
            iter2 += 1
        if (iter != 8 and iter2 != 8 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))
            if (self.chessArray[iter][iter2].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        iter = x + 1
        iter2 = y - 1
        # Check move down-left (x + 1, y - 1)        
        while (iter <= 7 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter += 1
            iter2 -= 1
        if (iter != 8 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))
            if (self.chessArray[iter][iter2].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        iter = x - 1
        iter2 = y - 1
        # Check move up-left (x - 1, y - 1)
        while (iter >= 0 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter -= 1
            iter2 -= 1
        if (iter != -1 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))
            if (self.chessArray[iter][iter2].get_name() == "k"): # Already the opposite color...
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")

        return possibleMoves
    
    def knightCheck(self, x, y, color):
        possibleMoves = []
        # No real way to iterate through this. Just check all eight spaces one at a time. 

        # Move up2, right 1 (x - 2, y + 1)
        if (x > 1 and y < 7 and (self.chessArray[x - 2][y + 1] == None or self.chessArray[x - 2][y + 1].get_color() != color)):
            possibleMoves.append((x - 2, y + 1))
        # Move up1, right 2 (x - 1, y + 2)
        if (x > 0 and y < 6 and (self.chessArray[x - 1][y + 2] == None or self.chessArray[x - 1][y + 2].get_color() != color)):
            possibleMoves.append((x - 1, y + 2))

        # Move down1, right 2 (x + 1, y + 2)
        if (x < 7 and y < 6 and (self.chessArray[x + 1][y + 2] == None or self.chessArray[x + 1][y + 2].get_color() != color)):
            possibleMoves.append((x + 1, y + 2))
        # Move down2, right 1 (x + 2, y + 1)
        if (x < 6 and y < 7 and (self.chessArray[x + 2][y + 1] == None or self.chessArray[x + 2][y + 1].get_color() != color)):
            possibleMoves.append((x + 2, y + 1))

        # Move down 2, left 1 (x + 2, y - 1)
        if (x < 6 and y > 0 and (self.chessArray[x + 2][y - 1] == None or self.chessArray[x + 2][y - 1].get_color() != color)):
            possibleMoves.append((x + 2, y - 1))
        # Move down 1, left 2 (x + 1, y - 2)
        if (x < 7 and y > 1 and (self.chessArray[x + 1][y - 2] == None or self.chessArray[x + 1][y - 2].get_color() != color)):
            possibleMoves.append((x + 1,y - 2))

        # Move up 1, left 2 (x - 1, y - 2)
        if (x > 0 and y > 1 and (self.chessArray[x - 1][y - 2] == None or self.chessArray[x - 1][y - 2].get_color() != color)):
            possibleMoves.append((x - 1, y - 2))
        # Move up 2, left 1 (x - 2, y -  1)
        if (x > 1 and y > 0 and (self.chessArray[x - 2][y - 1] == None or self.chessArray[x - 2][y - 1].get_color() != color)):
            possibleMoves.append((x - 2,y - 1))

        for x1, y1 in possibleMoves:
            if (self.chessArray[x1][y1] != None and self.chessArray[x1][y1].get_name() == "k"): # If it's not none, the piece must be the opposite color. 
                if (color == "white"):
                    self.blackKingCheck = True
                elif (color == "black"):
                    self.whiteKingCheck = True
                else:
                    print("???")
        return possibleMoves
    
    def kingCheck(self, x, y, color):
        possibleMoves = []
        # Similar to the knight check, just check all eight squares. 

        # Move up 1 (x - 1)
        if (x > 0 and (self.chessArray[x - 1][y] == None or self.chessArray[x - 1][y].get_color() != color)):
            possibleMoves.append((x - 1, y))
        # Move up 1, right 1 (x - 1, y + 1)
        if (x > 0 and y < 7 and (self.chessArray[x - 1][y + 1] == None or self.chessArray[x - 1][y + 1].get_color() != color)):
            possibleMoves.append((x - 1, y + 1))

        # Move right 1 (y + 1)
        if (y < 7 and (self.chessArray[x][y + 1] == None or self.chessArray[x][y + 1].get_color() != color)):
            possibleMoves.append((x, y + 1))
        # Move down 1, right 1 (x + 1, y + 1)
        if (x < 7 and y < 7 and (self.chessArray[x + 1][y + 1] == None or self.chessArray[x + 1][y + 1].get_color() != color)):
            possibleMoves.append((x + 1, y + 1))

        # Move down 1 (x + 1)
        if (x < 7 and (self.chessArray[x + 1][y] == None or self.chessArray[x + 1][y].get_color() != color)):
            possibleMoves.append((x + 1, y))
        # Move down 1, left 1 (x + 1, y - 1)
        if (x < 7 and y > 0 and (self.chessArray[x + 1][y - 1] == None or self.chessArray[x + 1][y - 1].get_color() != color)):
            possibleMoves.append((x + 1,y - 1))

        # Move left 1 (y - 1)
        if (y > 0 and (self.chessArray[x][y - 1] == None or self.chessArray[x][y - 1].get_color() != color)):
            possibleMoves.append((x, y - 1))
        # Move up 1, left 1 (x - 1, y -  1)
        if (x > 0 and y > 0 and (self.chessArray[x - 1][y - 1] == None or self.chessArray[x - 1][y - 1].get_color() != color)):
            possibleMoves.append((x - 1,y - 1))
        
        for x1, y1 in possibleMoves[:]:
            if (self.kingCheckCheck(x1, y1, color)):
                # print("KING DECTECTED")
                possibleMoves.remove((x1, y1))
        return possibleMoves
    
    def kingCheckCheck(self, x, y, color): # Checks for a king in the surrounding squares from the given location and returns True. 
        # Move up 1 (x - 1)
        if (x > 0 and self.chessArray[x - 1][y] != None and self.chessArray[x - 1][y].get_name() == "k" and self.chessArray[x - 1][y].get_color() != color):
            return True
        # Move up 1, right 1 (x - 1, y + 1)
        if (x > 0 and y < 7 and self.chessArray[x - 1][y + 1] != None and self.chessArray[x - 1][y + 1].get_name() == "k" and self.chessArray[x - 1][y + 1].get_color() != color):
            return True

        # Move right 1 (y + 1)
        if (y < 7 and self.chessArray[x][y + 1] != None and self.chessArray[x][y + 1].get_name() == "k" and self.chessArray[x][y + 1].get_color() != color):
            return True
        # Move down 1, right 1 (x + 1, y + 1)
        if (x < 7 and y < 7 and self.chessArray[x + 1][y + 1] != None and self.chessArray[x + 1][y + 1].get_name() == "k" and self.chessArray[x + 1][y + 1].get_color() != color):
            return True

        # Move down 1 (x + 1)
        if (x < 7 and self.chessArray[x + 1][y] != None and self.chessArray[x + 1][y].get_name() == "k" and self.chessArray[x + 1][y].get_color() != color):
            return True
        # Move down 1, left 1 (x + 1, y - 1)
        if (x < 7 and y > 0 and self.chessArray[x + 1][y - 1] != None and self.chessArray[x + 1][y - 1].get_name() == "k" and self.chessArray[x + 1][y - 1].get_color() != color):
            return True

        # Move left 1 (y - 1)
        if (y > 0 and self.chessArray[x][y - 1] != None and self.chessArray[x][y - 1].get_name() == "k" and self.chessArray[x][y - 1].get_color() != color):
            return True
        # Move up 1, left 1 (x - 1, y -  1)
        if (x > 0 and y > 0 and self.chessArray[x - 1][y - 1] != None and self.chessArray[x - 1][y - 1].get_name() == "k" and self.chessArray[x - 1][y - 1].get_color() != color):
            return True
        return False

    def whitePieceCheck(self):
        self.blackKingCheck = False
        for x, y in self.whitePieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                # Forwards movement
                if (x != 0 and self.chessArray[x - 1][y] == None):
                    possibleMoves.append((x - 1, y))
                    if (x != 1 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x - 2][y] == None):
                        possibleMoves.append((x - 2, y))
                
                # Capture Movement
                if (x != 0 and y != 0 and (self.chessArray[x - 1][y - 1] != None and self.chessArray[x - 1][y - 1].get_color() == "black")):
                    possibleMoves.append((x - 1, y - 1))
                    if (self.chessArray[x - 1][y - 1].get_name() == "k"):
                        self.blackKingCheck = True
                if (x != 0 and y != 7 and (self.chessArray[x - 1][y + 1] != None and self.chessArray[x - 1][y + 1].get_color() == "black")):
                    possibleMoves.append((x - 1, y + 1))
                    if (self.chessArray[x - 1][y + 1].get_name() == "k"):
                        self.blackKingCheck = True
            elif (self.chessArray[x][y].get_name() == "r"):
                possibleMoves = self.rookCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "b"):
                possibleMoves = self.bishopCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "q"): # maybe..?
                possibleMoves += self.rookCheck(x, y, "white")
                possibleMoves += self.bishopCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "kn"): 
                possibleMoves = self.knightCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "k"): 
                possibleMoves = self.kingCheck(x, y, "white")
            print("WHITE {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)

    def blackPieceCheck(self):
        self.whiteKingCheck = False
        for x, y in self.blackPieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                # Forwards movement
                if (x != 7 and self.chessArray[x + 1][y] == None):
                    possibleMoves.append((x + 1, y))
                    if (x != 6 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x + 2][y] == None):
                        possibleMoves.append((x + 2, y))
                
                # Capture Movement
                if (x != 7 and y != 0 and self.chessArray[x + 1][y - 1] != None and (self.chessArray[x + 1][y - 1].get_color() == "white")):
                    possibleMoves.append((x + 1, y - 1))
                    if (self.chessArray[x + 1][y - 1].get_name() == "k"):
                        self.whiteKingCheck = True
                if (x != 7 and y != 7 and self.chessArray[x + 1][y + 1] != None and (self.chessArray[x + 1][y + 1].get_color() == "white")):
                    possibleMoves.append((x + 1, y + 1))
                    if (self.chessArray[x + 1][y + 1].get_name() == "k"):
                        self.whiteKingCheck = True
            elif (self.chessArray[x][y].get_name() == "r"):
                possibleMoves = self.rookCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "b"):
                possibleMoves = self.bishopCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "q"): # maybe..?
                possibleMoves += self.rookCheck(x, y, "black")
                possibleMoves += self.bishopCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "kn"):
                possibleMoves = self.knightCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "k"): 
                possibleMoves = self.kingCheck(x, y, "black")
            print("BLACK {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
    def checkCheck(self):
        print(f"White in check? {self.whiteKingCheck}")
        print(f"Black in check? {self.blackKingCheck}")

# EN PASSANT CHECK: 
#     Capturing en passant is permitted only on the turn *immediately* 
#     after the two-square advance; it cannot be done on a later turn. 
# This means that a pawn needs a boolean or something so it knows it moved twice.

def PawnState(b):
    b.clear()
    b.addPiece(0, 1, "p", "white")
    b.addPiece(5, 2, "p", "white")
    b.chessArray[5][2].set_first_move()
    b.addPiece(6, 4, "p", "white")
    b.addPiece(6, 6,"p", "white")
    b.addPiece(2, 5,"p", "white")
    b.addPiece(6, 1,"p", "white")

    b.addPiece(4, 3, "p", "black")
    b.addPiece(1, 5, "p", "black")
    b.addPiece(4, 6, "p", "black")
    b.addPiece(5, 0, "p", "black")

def RookState(b):
    b.clear()
    b.addPiece(0, 0, "r", "white")
    b.addPiece(0, 7, "r", "white")
    b.addPiece(7, 0, "r", "black")
    b.addPiece(3, 7, "r", "white")
    b.addPiece(3, 3, "r", "white")
    b.addPiece(3, 5, "r", "black")
    
def BishopState(b):
    b.clear()
    b.addPiece(3, 3, "b", "white")
    b.addPiece(1, 5, "b", "white")
    b.addPiece(0, 0, "b", "black")
    b.addPiece(4, 2, "b", "black")
    b.addPiece(6, 6, "b", "white")

def QueenState(b):
    b.clear()
    b.addPiece(3, 3, "q", "white")
    b.addPiece(4, 4, "q", "black")

def KnightState(b):
    b.clear()
    b.addPiece(3, 3, "kn", "white")
    l = [(1, 4), (2, 5), (4, 5), (5, 4), (5, 2), (4, 1), (2, 1), (1, 2)]
    i = 0
    for x, y in l:
        c = "white"
        if (i % 2 == 0):
            c = "black"
        b.addPiece(x, y, "kn", c)
        i += 1

def KingState(b):
    b.clear()
    b.addPiece(0, 0, "k", "white")
    b.addPiece(1, 2, "k", "black")
    # b.addPiece()

def CheckState(b):
    b.clear()
    b.addPiece(0, 3, "k", "black")
    b.addPiece(1, 5, "k", "white")
    b.addPiece(7, 5, "r", "black")
    b.addPiece(3, 0, "b", "white")
    b.addPiece(2, 2, "kn", "white")
    b.addPiece(2, 4, "p", "black")
    b.addPiece(1, 4, "q", "black")
    b.addPiece(0, 5, "q", "white")

def main():
    newgame = board()
    CheckState(newgame)
    newgame.printBoardState()
    newgame.whitePieceCheck()
    newgame.blackPieceCheck()
    newgame.checkCheck()
main()