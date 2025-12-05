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
        self.en_passant_square = None   # For en passant check
        self.en_passant_pawn = None   # For en passant check
        
        # Automatically initialize start state
        if initialize: 
            #print("Loading tester.txt")
            self.loadPosition("test_positions/black_castling_queenside.txt")
            self.updateAllLegal()
            

    
    def loadPosition(self, filepath):
        # Piece map for easier access
        piece_map = {
            'p': ("p", "black"),
            'r': ("r", "black"),
            'n': ("kn", "black"),
            'b': ("b", "black"),
            'q': ("q", "black"),
            'k': ("k", "black"),
            'P': ("p", "white"),
            'R': ("r", "white"),
            'N': ("kn", "white"),
            'B': ("b", "white"),
            'Q': ("q", "white"),
            'K': ("k", "white")
        }

        # Open file and split into lines
        with open(filepath, "r") as f:
            lines = f.read().splitlines()

        # Go through each line and add the piece to the board 
        for i, row in enumerate(lines):
            for j, ch in enumerate(row):
                if ch == ".":
                    continue
                piece, color = piece_map[ch]
                self.addPiece(i, j, piece, color)



    def getKingLocation(self,color):
        if (color == "white"):
            return self.whiteKingXY
        if (color == "black"):
            return self.blackKingXY
        print("Invalid color")
        return (-1,-1)
        

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
        
        # Create a the piece object using the map and place in correct spot
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
        lookup = {"white":(self.whiteKingXY,self.blackPieces),
                  "black":(self.blackKingXY,self.whitePieces)}
        kinglocation,enemypieces = lookup[color]
        for piece in enemypieces:
            x,y = piece[0],piece[1]
            color2 = self.chessArray[x][y].get_color()
            if kinglocation in self.getPossibleMoves(x,y,color2):
                # print("King is in check by ", self.chessArray[x][y].get_color(),
                #        " " , self.chessArray[x][y].get_name(), " at " , x, ",", y)
                return True
        return False
    

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

    #Gets all possible moves (i.e. moves that aren't blocked by other pieces or don't send you off the board) subject to debuffs
    def getPossibleMoves(self,x,y,color):
        possibleMoves2 = []
        #print(self.chessArray[x][y].get_color()," ", self.chessArray[x][y].get_name(), " at ", x, "," , y)
        noncaptureMoves = self.chessArray[x][y].getPossibleNoncapture()
        captureMoves = self.chessArray[x][y].getPossibleCapture()

        # if (self.chessArray[x][y].get_name() == "q"):
        #     print (self.chessArray[x][y].get_color(), " ", self.chessArray[x][y].get_name())
        #     print("Noncapture moves: ", noncaptureMoves)
        #     print("Capture moves: ", captureMoves)
        # Line of sight check, stop if you hit a piece 
        for direction in noncaptureMoves:
            for lineofsight in direction:
                if (self.chessArray[lineofsight[0]][lineofsight[1]] != None):
                    break
                possibleMoves2.append(lineofsight)

        #print("PossibleMoves up to this point are ", possibleMoves2)
                
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

        # if (self.chessArray[x][y].get_name() == "q"):
        #     print("Now after debuffs ", possibleMoves2)

        if (self.chessArray[x][y].get_isDebuffed()):
            possibleMoves2 = self.chessArray[x][y].apply_debuff(possibleMoves2)
        #print("After filtering, the possible moves for ", self.chessArray[x][y], " at ", x, "," , y, "" ,
        #" are ", possibleMoves2)
        return possibleMoves2
            
    def getLegalMoves(self,x,y):
        legalMoves = []
        color = self.chessArray[x][y].get_color()
        possibleMoves = self.getPossibleMoves(x,y, color)

        # Castling shit 
        piece = self.chessArray[x][y]
        if piece.get_name() == "k":
            # white king 
            if color == "white" and (x, y) == (7, 4):
                # King-side 
                if self.chessArray[7][5] is None and self.chessArray[7][6] is None:
                    rook = self.chessArray[7][7]
                    if rook is not None and rook.get_name() == "r":
                        possibleMoves.append((7, 6))  # K to g1

                # Queen-side 
                if (self.chessArray[7][1] is None and
                    self.chessArray[7][2] is None and
                    self.chessArray[7][3] is None):
                    rook = self.chessArray[7][0]
                    if rook is not None and rook.get_name() == "r":
                        possibleMoves.append((7, 2))  

            # black king 
            elif color == "black" and (x, y) == (0, 4):
                # King-side 
                if self.chessArray[0][5] is None and self.chessArray[0][6] is None:
                    rook = self.chessArray[0][7]
                    if rook is not None and rook.get_name() == "r":
                        possibleMoves.append((0, 6)) 

                # Queen-side 
                if (self.chessArray[0][1] is None and
                    self.chessArray[0][2] is None and
                    self.chessArray[0][3] is None):
                    rook = self.chessArray[0][0]
                    if rook is not None and rook.get_name() == "r":
                        possibleMoves.append((0, 2))  
                        
        newboard = self.clone_board_state()
        for move in possibleMoves:
            if (newboard.moveprediction(move[0],move[1],x,y,color)):
                legalMoves.append(move)
        return legalMoves

    
    def returnLegalMoves(self,x,y):
        return self.chessArray[x][y].get_possible_moves()
    
    def updateAllLegal(self):
        self.updateLegal("white")
        self.updateLegal("black")
    
    # Iterates and updates legal moves for a color 
    def updateLegal(self, color):
        countMoves = 0
        # Check if in check 
        if(self.isKinginCheck(color)):
            print(color, "king in check")
        
        # Get specific piece list based on color 
        pieceList = self.whitePieces.copy() if color == "white" else self.blackPieces.copy()
        
        # Go through piece list to get legal moves 
        for x, y in pieceList:
            legalMoves = self.getLegalMoves(x, y)
            countMoves += len(legalMoves)
            self.chessArray[x][y].updateLegalMoves(legalMoves)
        return countMoves
    

    def clone_board_state(self):
        # Set up a plane new board
        new_board = board(False)
        new_board.chessArray = [[None for j in range(8)] for i in range(8)]
        new_board.whitePieces = []
        new_board.blackPieces = []
        
        # Iterate through the old board and copy over 
        for i in range(8):
            for j in range(8):
                piece = self.chessArray[i][j]
                if piece:
                    new_board.addPiece(i, j, piece.name, piece.color)
                    if (piece.color == "white"):
                        new_board.whitePieces.append((i,j))
                    if (piece.color == "black"):
                        new_board.blackPieces.append((i,j))
        return new_board
    

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
        self.chessArray[newx][newy].update_coordinates(newx,newy)
        self.chessArray[newx][newy].firstMove = False
        self.chessArray[oldx][oldy] = None
        self.chessArray[newx][newy].findMoves(newx,newy)

        if (self.blackKingXY == (oldx,oldy)):
            self.blackKingXY = newx,newy
        if (self.whiteKingXY == (oldx,oldy)):
            self.whiteKingXY = newx,newy
       
        # brute-force rook movement
        moved_piece = self.chessArray[newx][newy]
        # King must be moving
        if moved_piece.get_name() == "k":
            # King-side castling
            if oldy == 4 and newy == 6:
                # White rook movement 
                if color == "white" and oldx == 7:
                    rook = self.chessArray[7][7]
                    self.chessArray[7][7] = None
                    self.chessArray[7][5] = rook
                    self.whitePieces.remove((7,7))
                    self.whitePieces.append((7,5))
                    rook.findMoves(7,5)

                # Black rook movement
                if color == "black" and oldx == 0:
                    rook = self.chessArray[0][7]
                    self.chessArray[0][7] = None
                    self.chessArray[0][5] = rook
                    self.blackPieces.remove((0,7))
                    self.blackPieces.append((0,5))
                    rook.findMoves(0,5)

            # Queen-side castling 
            if oldy == 4 and newy == 2:
                # White rook movement
                if color == "white" and oldx == 7:
                    rook = self.chessArray[7][0]
                    self.chessArray[7][0] = None
                    self.chessArray[7][3] = rook
                    self.whitePieces.remove((7,0))
                    self.whitePieces.append((7,3))
                    rook.findMoves(7,3)

                # Black rook from movement
                if color == "black" and oldx == 0:
                    rook = self.chessArray[0][0]
                    self.chessArray[0][0] = None
                    self.chessArray[0][3] = rook
                    self.blackPieces.remove((0,0))
                    self.blackPieces.append((0,3))
                    rook.findMoves(0,3)


