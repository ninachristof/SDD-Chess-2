from chesspiece import *
import time
import copy 
class board:

    ##################################################################################
    ##################################################################################
    #EVERYTHING HERE IS PRIVATE
    #NOTHING OUTSIDE OF THE BOARD CLASS SHOULD BE CALLING THESE FUNCTIONS
    ##################################################################################
    ##################################################################################

    
    def __init__(self, initialize): 
        #print("INITIALIZEING BOARD")
        self.chessArray = [[None for j in range(8)] for i in range(8)]
        self.whitePieces = [] # The list of locations for white pieces
        self.blackPieces = [] # The list of locations for black pieces
        
        # Automatically initialize start state
        if initialize: 
            self.startState()
    
    def startState(self):
        self.clear()
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

        #self.updateAllPieces()
        

    # Reset board and remove all pieces. 
    def clear(self):
        self.chessArray = [[None for j in range(8)] for i in range(8)]
        self.whitePieces = []
        self.blackPieces = []
         
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

        # Create a map of all the pieces for easier initialization 
        piece_map = {
            "p": pawn,
            "kn": knight,
            "r": rook,
            "b": bishop,
            "q": queen,
            "k": king
        }
        
        if piece not in piece_map:
            print(f"Invalid piece name: {piece}")
            return
        
        piece_obj = piece_map[piece](x, y, color)
        self.chessArray[x][y] = piece_obj
        if color == "white":
            self.whitePieces.append((x, y))
            if piece == 'k': self.whiteKingXY = (x, y)
        else:
            self.blackPieces.append((x, y))
            if piece == 'k': self.blackKingXY = (x, y)
        
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
    
    
    #Checks if the king that of the inputted color is in check
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
        #print(x,y)
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
            pieceFound = False
            temp = []
            for lineofsight in direction:
                if (self.chessArray[lineofsight[0]][lineofsight[1]] != None):
                    if (self.chessArray[lineofsight[0]][lineofsight[1]].get_color() != color):
                        pieceFound = True
                        temp.append(lineofsight)
                    break
                temp.append(lineofsight)
            if (not self.chessArray[x][y].get_captureOnlyWithPiece() or pieceFound):
                possibleMoves2.extend(temp)
        #print(f"{self.chessArray[x][y].get_name()}: at {x}, {y}: {possibleMoves2}")
        #print("AAA: ", possibleMoves2)
        return possibleMoves2

    
    def updateAllPieces(self):
        self.updatePieces("white")
        self.updatePieces("black")

    def updatePieces(self, color):
        pieces = self.whitePieces if color == "white" else self.blackPieces
        for (x, y) in pieces:
            piece = self.chessArray[x][y]
            if not piece:
                continue
            moves = self.getPossibleMoves(x, y, color)
            piece.updatePossibleMoves(moves)
            
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
            #print("white ", self.chessArray[x][y].get_name(), " at ", x, ",",y)
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


    def clone_board_state(self):
        #print("In here:")
        new_board = board(False)
        #print("END here:")
        new_board.chessArray = [[None for j in range(8)] for i in range(8)]
        new_board.whitePieces = []
        new_board.blackPieces = []
        for i in range(8):
            for j in range(8):
                piece = self.chessArray[i][j]
               # print(" NEW PIECE", piece)
                if piece:
                    new_board.addPiece(i, j, piece.name, piece.color)
        return new_board

    
    

    def moveprediction(self,newx,newy,oldx,oldy,color):
        temp = self.chessArray[newx][newy]
        # Are you landing on a square that's the same color as you? If so, return False
        if (temp != None and temp.get_color() == color):
            return False
        
        # Checks if this move is valid; i.e. the king is not in check after this move
        clone = self.clone_board_state()
        validMove = False
        clone.movePiece(newx,newy,oldx,oldy,color, False)
        if (not clone.isKinginCheck(color)):
            validMove = True
        return validMove
        

    def movePiece(self, newx, newy, oldx, oldy, color, update):
        # Check if location empty 
        if self.chessArray[oldx][oldy] is None:
            return
        
        # Create a dic for easier usage
        piece_lists = {
            "white": (self.whitePieces, self.blackPieces),
            "black": (self.blackPieces, self.whitePieces)
        } 
        
        # Remove piece from own list and opp if needed, and add new piece to own 
        ownList, oppList = piece_lists[color]
        ownList.remove((oldx, oldy))
        if (newx, newy) in oppList: 
            oppList.remove((newx, newy))
        ownList.append((newx, newy))

        # Update board object 
        self.chessArray[newx][newy] = self.chessArray[oldx][oldy]
        self.chessArray[oldx][oldy] = None
        
        # Test for if we are actually moving the piece or just simulating, dont update pieces if the latter
        # to avoid overhead
        if(update): self.updateAllPieces()
            


# EN PASSANT CHECK: 
#     Capturing en passant is permitted only on the turn *immediately* 
#     after the two-square advance; it cannot be done on a later turn. 
# This means that a pawn needs a boolean or something so it knows it moved twice.
