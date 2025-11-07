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

    def startState(self, color): # Initial board setup. 
        # Initialize Pawns
        #if(color == "white"):
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
                        #print("White King in check")
                        return True
            #print("White King not in check")
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
                        #print("Black King in check")
                        return True
            #print("Black King not in check")
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
        if (i < 0 or j < 0 or i > 7 or j > 7):
            print("Not on board!")
            return None
        return self.chessArray[i][j]

    #Gets all possible moves (i.e. moves that aren't blocked by other pieces or don't send you off the board)
    def getPossibleMoves(self,x,y,color):
        #print("getting possible moves for ", x, "," , y)
        #print(f"{self.chessArray[x][y].get_name()}: at {x}, {y}: {self.chessArray[x][y].findMoves(x, y)}")
        #return [self.chessArray[x][y].findMoves(x, y)]
        possibleMoves2 = []
        noncaptureMoves = self.chessArray[x][y].findMoves(x,y)[0]
        captureMoves = self.chessArray[x][y].findMoves(x, y)[1]
        #if (self.chessArray[x][y].get_name() == "kn"):
            #print(x, ",",y)
            #print("capture moves: ", captureMoves)
            #print("noncapture moves: ", captureMoves)
        for direction in noncaptureMoves:
            for lineofsight in direction:
                if (self.chessArray[lineofsight[0]][lineofsight[1]] != None):
                    break
                possibleMoves2.append(lineofsight)

        for direction in captureMoves:
            for lineofsight in direction:
                if (self.chessArray[lineofsight[0]][lineofsight[1]] != None):
                    if (self.chessArray[lineofsight[0]][lineofsight[1]].get_color() != color):
                        possibleMoves2.append(lineofsight)
                    break
                possibleMoves2.append(lineofsight)
        #print(f"{self.chessArray[x][y].get_name()}: at {x}, {y}: {possibleMoves2}")
        #print("AAA: ", possibleMoves2)
        return possibleMoves2
    
        # possibleMoves = []
        # color = self.chessArray[x][y].get_color()
        # if (self.chessArray[x][y].get_name() == "p"): # Pawn
        #     possibleMoves = self.getPawnMoves(x, y, color)
        # elif (self.chessArray[x][y].get_name() == "r"): # Rook
        #     possibleMoves = self.getRookMoves(x, y, color)
        # elif (self.chessArray[x][y].get_name() == "b"): # Bishop
        #     possibleMoves = self.getBishopMoves(x, y, color)
        # elif (self.chessArray[x][y].get_name() == "q"): # Queen
        #     possibleMoves += self.getRookMoves(x, y, color)
        #     possibleMoves += self.getBishopMoves(x, y, color)
        # elif (self.chessArray[x][y].get_name() == "kn"): # Knight
        #     possibleMoves = self.getKnightMoves(x, y, color)
        # elif (self.chessArray[x][y].get_name() == "k"): # King
        #     possibleMoves = self.getKingMoves(x, y, color)
        # print(f"{self.chessArray[x][y].get_name()}: at {x}, {y}: {possibleMoves}")
        # return possibleMoves
    
    # Iterates through each white piece location and updates the pieces with the new available moves. 
    def whitePieceUpdate(self):
        for x, y in self.whitePieces:
            #print("piece at ", x , ",", y)
            possibleMoves = self.getPossibleMoves(x,y, "white")
            #print("WHITE {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            #print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves) # Updates the moves of the piece.
        #self.isKinginCheck("white")

    # Same as whitePieceCheck, but for the black pieces. 
    def blackPieceUpdate(self):
        for x, y in self.blackPieces:
            #print("piece at ", x , ",", y)
            possibleMoves = self.getPossibleMoves(x,y, "black")
            #print("BLACK {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            #print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
        #self.isKinginCheck("black")

    def getLegalMoves(self,x,y):
        legalMoves = []
        color = self.chessArray[x][y].get_color()
        possibleMoves = self.getPossibleMoves(x,y, color)
        #print("Possible moves are", possibleMoves)
        #legalMoves = possibleMoves
        for move in possibleMoves:
            if (self.moveprediction(move[0],move[1],x,y,color)):
                legalMoves.append(move)
            # self.movePiece(move[0],move[1],x,y,color)
            # if (not self.isKinginCheck(color)):
            #     legalMoves.append(move)
            # self.movePiece(x,y,move[0],move[1],color)
        return legalMoves
    
    def returnLegalMoves(self,x,y):
        return self.chessArray[x][y].get_possible_moves()
    
    # Iterates through each white piece location and updates the pieces with the new available moves. 
    def whitePieceUpdateLegal(self):
        countMoves = 0
        if (self.isKinginCheck("white")):
            print("White king in check")
        for x, y in self.whitePieces:
            print("white ", self.chessArray[x][y].get_name(), " at ", x, ",",y)
            possibleMoves = self.getLegalMoves(x,y)
            countMoves += len(possibleMoves)
            print("legal moves are ", possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves) # Updates the moves of the piece.
        return countMoves
        #self.isKinginCheck("white")

    # Same as whitePieceCheck, but for the black pieces. 
    def blackPieceUpdateLegal(self):
        countMoves = 0
        if (self.isKinginCheck("black")):
            print("Black king in check")
        for x, y in self.blackPieces:
            print("black ", self.chessArray[x][y].get_name(), " at ", x, ",",y)
            possibleMoves = self.getLegalMoves(x,y)
            countMoves += len(possibleMoves)
            print("legal moves are ", possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
        return countMoves
        #self.isKinginCheck("black")

    def moveprediction(self,newx,newy,oldx,oldy,color):

        #Stores the deleted square if necessary
        temp = self.chessArray[newx][newy]
        #Are you landing on a square that's the same color as you? If so, return False
        if (temp != None and temp.get_color() == color):
            return False
        
        #checks if this move is valid; i.e. the king is not in check after this move
        validMove = False
        self.movePiece(newx,newy,oldx,oldy,color)
        if (not self.isKinginCheck(color)):
            validMove = True
        #Undoes any of the effects of the move
        self.movePiece(oldx,oldy,newx,newy,color)
        if (temp == None):
            return validMove
        
        #Resurrects the dead piece if the square we moved to wasn't none
        color = temp.get_color()
        if (color == "white"):
            self.whitePieces.append((newx,newy))
            self.chessArray[newx][newy] = temp
        if (color == "black"):
            self.blackPieces.append((newx,newy))
            self.chessArray[newx][newy] = temp
        return validMove
        

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
        # if (self.isKinginCheck("white")):
        #     print("White king in check")
        # if (self.isKinginCheck("black")):
        #     print("Black king in check")

# EN PASSANT CHECK: 
#     Capturing en passant is permitted only on the turn *immediately* 
#     after the two-square advance; it cannot be done on a later turn. 
# This means that a pawn needs a boolean or something so it knows it moved twice.
