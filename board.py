from chesspiece import *
import time
class board:

    ##################################################################################
    ##################################################################################
    #EVERYTHING HERE IS PRIVATE
    #NOTHING OUTSIDE OF THE BOARD CLASS SHOULD BE CALLING THESE FUNCTIONS
    ##################################################################################
    ##################################################################################

    chessArray = [[None for j in range(8)] for i in range(8)]
    whitePieces = [] # The list of locations for white pieces
    blackPieces = [] # The list of locations for black pieces

    def addPiece(self, x, y, piece, color):
        # The coordinates of this are a little messed up. 
        # Current system: X is vertical going downwards, Y is horizontal going Right.

        # Valid coordinates check.
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate.")
            return
        # Valid color check.
        if (color != "black" and color != "white"):
            print(f"{color} is not a valid color.")
            return

        # Empty square check.
        if (self.chessArray[x][y] != None):
            print(f"The {color} {piece} piece cannot be placed at ({x}, {y}) because there is already a {self.chessArray[x][y].get_color()} {self.chessArray[x][y].get_name()} piece there")
            return

        # Piece check and placement.
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
            if (color == "white"):
                self.whiteKingXY = (x, y)
            else:
                self.blackKingXY = (x, y)
        else:
            print(f"{piece} is not a valid piece. Try again.")
            return

        # Adding the piece to the appropriate color list. 
        if (color == "white"):
            self.whitePieces.append((x, y))
        else:
            self.blackPieces.append((x, y))

    # Reset board and remove all pieces. 
    def clear(self):
        self.chessArray = [[None for j in range(8)] for i in range(8)]
        self.whitePieces = []
        self.blackPieces = []

    # Print the board.
    def printBoardState(self):
        print("  ", end="") 
        for i in range(8):
            print(f"|  {i} ", end="")
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
    
    def getPawnMoves(self, x, y, color):
        possibleMoves = []
        if (color == "white"):
            # Forwards movement
            if (x != 0 and self.chessArray[x - 1][y] == None):
                possibleMoves.append((x - 1, y))
                if (x != 1 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x - 2][y] == None):
                    possibleMoves.append((x - 2, y))
            
            # Capture Movement
            if (x != 0 and y != 0 and (self.chessArray[x - 1][y - 1] != None and self.chessArray[x - 1][y - 1].get_color() == "black")):
                possibleMoves.append((x - 1, y - 1))
            if (x != 0 and y != 7 and (self.chessArray[x - 1][y + 1] != None and self.chessArray[x - 1][y + 1].get_color() == "black")):
                possibleMoves.append((x - 1, y + 1))
        else:
            # Forwards movement
            if (x != 7 and self.chessArray[x + 1][y] == None):
                possibleMoves.append((x + 1, y))
                if (x != 6 and (self.chessArray[x][y].hasMoved()) and self.chessArray[x + 2][y] == None):
                    possibleMoves.append((x + 2, y))
            
            # Capture Movement
            if (x != 7 and y != 0 and self.chessArray[x + 1][y - 1] != None and (self.chessArray[x + 1][y - 1].get_color() == "white")):
                possibleMoves.append((x + 1, y - 1))
            if (x != 7 and y != 7 and self.chessArray[x + 1][y + 1] != None and (self.chessArray[x + 1][y + 1].get_color() == "white")):
                possibleMoves.append((x + 1, y + 1))
        return possibleMoves

    # Rook movement check. 
    # Assumptions: There is a <white/black> piece at x, y that moves orthogonally. 
    def getRookMoves(self, x, y, color): 
        if (color != "white" and color != "black"):
            print("Invalid color in getRookMoves")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in getRookMoves")
            return []

        possibleMoves = []

        # Check move upwards (x - 1)
        iter = x - 1
        while (iter >= 0 and (self.chessArray[iter][y] == None)):
            # While the iter is still on the board AND the square is empty...
            possibleMoves.append((iter, y)) # Add the square to the possible moves. 
            iter -= 1 # Move up. 
        # Capture check.
        if (iter != -1 and self.chessArray[iter][y].get_color() != color):
            # If the iter is still on the board and the associated square is the opposite color...
            possibleMoves.append((iter, y))  # Add the square with that piece to the board. 
        # Repeat with the other four directions. 

        iter = y + 1
        # Check move right (y + 1)
        while (iter <= 7 and (self.chessArray[x][iter] == None)):
            possibleMoves.append((x, iter))
            iter += 1
        if (iter != 8 and self.chessArray[x][iter].get_color() != color):
            possibleMoves.append((x, iter))

        iter = x + 1
        # Check move downwards (x + 1)
        while (iter <= 7 and (self.chessArray[iter][y] == None)):
            possibleMoves.append((iter, y))
            iter += 1
        if (iter != 8 and self.chessArray[iter][y].get_color() != color):
            possibleMoves.append((iter, y))
        
        iter = y - 1
        # Check move left (y - 1)
        while (iter >= 0 and (self.chessArray[x][iter] == None)):
            possibleMoves.append((x, iter))
            iter -= 1
        if (iter != -1 and self.chessArray[x][iter].get_color() != color):
            possibleMoves.append((x, iter))

        return possibleMoves
    
    # Bishop movement check. 
    # Assumptions: There is a <white/black> piece at x, y that moves diagonally.
    def getBishopMoves(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in getBishopMoves")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in getBishopMoves")
            return []
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

        iter = x + 1
        iter2 = y + 1
        # Check move down-right (x + 1, y + 1)
        while (iter <= 7 and iter2 <= 7 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter += 1
            iter2 += 1
        if (iter != 8 and iter2 != 8 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))

        iter = x + 1
        iter2 = y - 1
        # Check move down-left (x + 1, y - 1)        
        while (iter <= 7 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter += 1
            iter2 -= 1
        if (iter != 8 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))

        iter = x - 1
        iter2 = y - 1
        # Check move up-left (x - 1, y - 1)
        while (iter >= 0 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMoves.append((iter, iter2))
            iter -= 1
            iter2 -= 1
        if (iter != -1 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMoves.append((iter, iter2))
        return possibleMoves
    
    def getKnightMoves(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in getKnightMoves")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in getKnightMoves")
            return []
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
        return possibleMoves
    
    def getKingMoves(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in getKingMoves")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in getKingMoves")
            return []
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
        return possibleMoves
    

    #Checks if the king that is the inputted color is in check
    def isKinginCheck(self,color):
        kinglocation = 0,0
        if (color == "white"):
            for piece in self.whitePieces:
                #print(piece)
                if self.chessArray[piece[0]][piece[1]].get_name() == 'k':
                        kinglocation = piece[0],piece[1]
            for piece in self.blackPieces:
                #print(self.chessArray[piece[0]][piece[1]].get_color(), " ",
                      #self.chessArray[piece[0]][piece[1]].get_name(), " at ",
                      #piece[0], ",", piece[1])
                for move in self.chessArray[piece[0]][piece[1]].get_possible_moves():
                    #print(move)
                    if (move[0] == kinglocation[0] and move[1] == kinglocation[1]):
                        print("White King in check")
                        return True
            print("White King not in check")
            return False

        
        if (color == "black"):
            for piece in self.blackPieces:
                #print(piece)
                if self.chessArray[piece[0]][piece[1]].get_name() == 'k':
                        kinglocation = piece[0],piece[1]
            for piece in self.whitePieces:
                # print(self.chessArray[piece[0]][piece[1]].get_color(), " ",
                #       self.chessArray[piece[0]][piece[1]].get_name(), " at ",
                #       piece[0], ",", piece[1])
                for move in self.chessArray[piece[0]][piece[1]].get_possible_moves():
                    #print(move)
                    if (move[0] == kinglocation[0] and move[1] == kinglocation[1]):
                        print("Black King in check")
                        return True
            print("Black King not in check")
            return False
        #print("The king is at ", kinglocation)


    ##################################################################################
    ##################################################################################
    #Start of our public functions
    ##################################################################################
    ##################################################################################
    
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

        self.whitePieceUpdate()
        self.blackPieceUpdate()

    def getSquare(self,i,j):
        return self.chessArray[i][j]

    #Gets all possible moves (i.e. moves that aren't blocked by other pieces or don't send you off the board)
    def getPossibleMoves(self,x,y):
        possibleMoves = []
        color = self.chessArray[x][y].get_color()
        if (self.chessArray[x][y].get_name() == "p"): # Pawn
            possibleMoves = self.getPawnMoves(x, y, color)
        elif (self.chessArray[x][y].get_name() == "r"): # Rook
            possibleMoves = self.getRookMoves(x, y, color)
        elif (self.chessArray[x][y].get_name() == "b"): # Bishop
            possibleMoves = self.getBishopMoves(x, y, color)
        elif (self.chessArray[x][y].get_name() == "q"): # Queen
            possibleMoves += self.getRookMoves(x, y, color)
            possibleMoves += self.getBishopMoves(x, y, color)
        elif (self.chessArray[x][y].get_name() == "kn"): # Knight
            possibleMoves = self.getKnightMoves(x, y, color)
        elif (self.chessArray[x][y].get_name() == "k"): # King
            possibleMoves = self.getKingMoves(x, y, color)
        return possibleMoves
    
    # Iterates through each white piece location and updates the pieces with the new available moves. 
    def whitePieceUpdate(self):
        for x, y in self.whitePieces:
            #print("piece at ", x , ",", y)
            possibleMoves = self.getPossibleMoves(x,y)
            #print("WHITE {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            #print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves) # Updates the moves of the piece.
        self.isKinginCheck("white")

    # Same as whitePieceCheck, but for the black pieces. 
    def blackPieceUpdate(self):
        for x, y in self.blackPieces:
            #print("piece at ", x , ",", y)
            possibleMoves = self.getPossibleMoves(x,y)
            #print("BLACK {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            #print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
        self.isKinginCheck("black")

    def getLegalMoves(self,x,y):
        possibleMoves = self.getPossibleMoves(x,y)
        legalMoves = []
        color = self.chessArray[x][y].get_color()
        for move in possibleMoves:
            self.movePiece(move[0],move[1],x,y,color)
            if (not self.isKinginCheck(color)):
                legalMoves.append(move)
            self.movePiece(x,y,move[0],move[1],color)
        return legalMoves
    
    # Iterates through each white piece location and updates the pieces with the new available moves. 
    def whitePieceUpdateLegal(self):
        for x, y in self.whitePieces:
            possibleMoves = self.getLegalMoves(x,y)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves) # Updates the moves of the piece.
        self.isKinginCheck("white")

    # Same as whitePieceCheck, but for the black pieces. 
    def blackPieceUpdateLegal(self):
        for x, y in self.blackPieces:
            possibleMoves = self.getLegalMoves(x,y)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
        self.isKinginCheck("black")

    

    
    def movePiece(self,newx,newy,oldx,oldy,color):
        #print(self.whitePieces)
        #print(self.blackPieces)
        #print(oldx, " ", oldy , " ",newx, " ", newy, " ",color)
        if (color == "white"):
            self.whitePieces.remove((oldx,oldy))
            if ((newx,newy) in self.blackPieces):
                self.blackPieces.remove((newx,newy))
            self.whitePieces.append((newx,newy))
        else:
            self.blackPieces.remove((oldx,oldy))
            if ((newx,newy) in self.whitePieces):
                self.whitePieces.remove((newx,newy))
            self.blackPieces.append((newx,newy))
        self.chessArray[newx][newy] = self.chessArray[oldx][oldy]
        self.chessArray[oldx][oldy] = None
        self.whitePieceUpdate()
        self.blackPieceUpdate()

# EN PASSANT CHECK: 
#     Capturing en passant is permitted only on the turn *immediately* 
#     after the two-square advance; it cannot be done on a later turn. 
# This means that a pawn needs a boolean or something so it knows it moved twice.