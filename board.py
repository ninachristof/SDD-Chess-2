from chesspiece import *

class board:
    chessArray = [[None for j in range(8)] for i in range(8)]
    whitePieces = [] # The list of locations for white pieces
    blackPieces = [] # The list of locations for black pieces

    whiteKingXY = ()
    blackKingXY = ()

    def getSquare(self,i,j):
        return self.chessArray[i][j]
    

    def movePiece(self,newx,newy,oldx,oldy,color):
        print(self.whitePieces)
        print(self.blackPieces)
        print(oldx, " ", oldy , " ",newx, " ", newy, " ",color)
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

    def copy_board(self):
        board2 = board()
        for x, y in self.whitePieces:
            board2.addPiece(x, y, self.chessArray[x][y].get_name(), "white")
        for x, y in self.blackPieces:
            board2.addPiece(x, y, self.chessArray[x][y].get_name(), "black")
        return board2

    # Replaces the square at x, y with None
    def __clearSquare(self, x, y):
        if (x >= 0 and x <= 7 and y >= 0 and y <= 7):
            self.chessArray[x][y] = None

    def startState(self): # Initial board setup. 
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

    # Reset board and remove all pieces. 
    def clear(self):
        self.chessArray = [[None for j in range(8)] for i in range(8)]
        self.whitePieces = []
        self.blackPieces = []
        self.whiteKingXY = ()
        self.blackKingXY = ()

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
    
    def pawnCheck(self, x, y, color):
        forwardMoves = []
        captureMoves = []
        if (color == "white"):
            # Forwards movement
            if (x != 0 and self.chessArray[x - 1][y] == None):
                forwardMoves.append((x - 1, y))
                if (x != 1 and self.chessArray[x][y] != None and self.chessArray[x][y].hasMoved() and self.chessArray[x - 2][y] == None):
                    forwardMoves.append((x - 2, y))
            
            # Capture Movement
            if (x != 0 and y != 0 and (self.chessArray[x - 1][y - 1] != None and self.chessArray[x - 1][y - 1].get_color() == "black")):
                captureMoves.append((x - 1, y - 1))
            if (x != 0 and y != 7 and (self.chessArray[x - 1][y + 1] != None and self.chessArray[x - 1][y + 1].get_color() == "black")):
                captureMoves.append((x - 1, y + 1))
        else:
            # Forwards movement
            if (x != 7 and self.chessArray[x + 1][y] == None):
                forwardMoves.append((x + 1, y))
                if (x != 6 and self.chessArray[x][y] != None and (self.chessArray[x][y].hasMoved()) and self.chessArray[x + 2][y] == None):
                    forwardMoves.append((x + 2, y))
            
            # Capture Movement
            if (x != 7 and y != 0 and self.chessArray[x + 1][y - 1] != None and (self.chessArray[x + 1][y - 1].get_color() == "white")):
                captureMoves.append((x + 1, y - 1))
            if (x != 7 and y != 7 and self.chessArray[x + 1][y + 1] != None and (self.chessArray[x + 1][y + 1].get_color() == "white")):
                captureMoves.append((x + 1, y + 1))
        return [forwardMoves, captureMoves]


    # Rook movement check. SETS EACH DIRECTION INTO A SEPARATE LIST
    # Assumptions: There is a <white/black> piece at x, y that moves orthogonally. 
    def rookCheck(self, x, y, color): 
        if (color != "white" and color != "black"):
            print("Invalid color in rookCheck")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in rookCheck")
            return []

        possibleMovesUP = []
        # Check move upwards (x - 1)
        iter = x - 1
        while (iter >= 0 and (self.chessArray[iter][y] == None)):
            # While the iter is still on the board AND the square is empty...
            possibleMovesUP.append((iter, y)) # Add the square to the possible moves. 
            iter -= 1 # Move up. 
        # Capture check.
        if (iter != -1 and self.chessArray[iter][y].get_color() != color):
            # If the iter is still on the board and the associated square is the opposite color...
            possibleMovesUP.append((iter, y))  # Add the square with that piece to the board. 
        # Repeat with the other four directions. 

        possibleMovesRIGHT = []
        iter = y + 1
        # Check move right (y + 1)
        while (iter <= 7 and (self.chessArray[x][iter] == None)):
            possibleMovesRIGHT.append((x, iter))
            iter += 1
        if (iter != 8 and self.chessArray[x][iter].get_color() != color):
            possibleMovesRIGHT.append((x, iter))

        possibleMovesDOWN = []
        iter = x + 1
        # Check move downwards (x + 1)
        while (iter <= 7 and (self.chessArray[iter][y] == None)):
            possibleMovesDOWN.append((iter, y))
            iter += 1
        if (iter != 8 and self.chessArray[iter][y].get_color() != color):
            possibleMovesDOWN.append((iter, y))
        
        possibleMovesLEFT = []
        iter = y - 1
        # Check move left (y - 1)
        while (iter >= 0 and (self.chessArray[x][iter] == None)):
            possibleMovesLEFT.append((x, iter))
            iter -= 1
        if (iter != -1 and self.chessArray[x][iter].get_color() != color):
            possibleMovesLEFT.append((x, iter))

        return [possibleMovesUP, possibleMovesRIGHT, possibleMovesDOWN, possibleMovesLEFT]
    
    # Bishop movement check. 
    # Assumptions: There is a <white/black> piece at x, y that moves diagonally.
    def bishopCheck(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in bishopCheck")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in bishopCheck")
            return []
        possibleMovesUPRIGHT = []
        iter = x - 1
        iter2 = y + 1
        # Check move up-right (x - 1, y + 1)
        while (iter >= 0 and iter2 <= 7 and (self.chessArray[iter][iter2] == None)):
            possibleMovesUPRIGHT.append((iter, iter2))
            iter -= 1
            iter2 += 1
        if (iter != -1 and iter2 != 8 and self.chessArray[iter][iter2].get_color() != color):
            possibleMovesUPRIGHT.append((iter, iter2))

        possibleMovesDOWNRIGHT = []
        iter = x + 1
        iter2 = y + 1
        # Check move down-right (x + 1, y + 1)
        while (iter <= 7 and iter2 <= 7 and (self.chessArray[iter][iter2] == None)):
            possibleMovesDOWNRIGHT.append((iter, iter2))
            iter += 1
            iter2 += 1
        if (iter != 8 and iter2 != 8 and self.chessArray[iter][iter2].get_color() != color):
            possibleMovesDOWNRIGHT.append((iter, iter2))

        possibleMovesDOWNLEFT = []
        iter = x + 1
        iter2 = y - 1
        # Check move down-left (x + 1, y - 1)        
        while (iter <= 7 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMovesDOWNLEFT.append((iter, iter2))
            iter += 1
            iter2 -= 1
        if (iter != 8 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMovesDOWNLEFT.append((iter, iter2))

        possibleMovesUPLEFT = []
        iter = x - 1
        iter2 = y - 1
        # Check move up-left (x - 1, y - 1)
        while (iter >= 0 and iter2 >= 0 and (self.chessArray[iter][iter2] == None)):
            possibleMovesUPLEFT.append((iter, iter2))
            iter -= 1
            iter2 -= 1
        if (iter != -1 and iter2 != -1 and self.chessArray[iter][iter2].get_color() != color):
            possibleMovesUPLEFT.append((iter, iter2))
        return [possibleMovesUPRIGHT, possibleMovesDOWNRIGHT, possibleMovesDOWNLEFT, possibleMovesUPLEFT]
    
    def knightCheck(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in knightCheck")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in knightCheck")
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
        return [possibleMoves]
    
    def kingCheck(self, x, y, color):
        if (color != "white" and color != "black"):
            print("Invalid color in kingCheck")
            return []
        
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate in kingCheck")
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
        
        for x1, y1 in possibleMoves[:]:
            if (self.kingCheckCheck(x1, y1, color)):
                # print("KING DECTECTED")
                possibleMoves.remove((x1, y1))
        return [possibleMoves]
    
    def kingCheckCheck(self, x, y, color): 
        # Checks for an opposite color king in the surrounding squares from the given location and returns True if there is one. 
        # This is because a king cannot move into capturable range of another king. 

        # Statement breakdown: (Coordinates are within board) and (chessArray square is not empty) and (chessArray piece is a king) and (chessArray color is the opposite color)

        # Check up 1 (x - 1)
        if (x > 0 and self.chessArray[x - 1][y] != None and self.chessArray[x - 1][y].get_name() == "k" and self.chessArray[x - 1][y].get_color() != color):
            return True
        # Check up 1, right 1 (x - 1, y + 1)
        if (x > 0 and y < 7 and self.chessArray[x - 1][y + 1] != None and self.chessArray[x - 1][y + 1].get_name() == "k" and self.chessArray[x - 1][y + 1].get_color() != color):
            return True

        # Check right 1 (y + 1)
        if (y < 7 and self.chessArray[x][y + 1] != None and self.chessArray[x][y + 1].get_name() == "k" and self.chessArray[x][y + 1].get_color() != color):
            return True
        # Check down 1, right 1 (x + 1, y + 1)
        if (x < 7 and y < 7 and self.chessArray[x + 1][y + 1] != None and self.chessArray[x + 1][y + 1].get_name() == "k" and self.chessArray[x + 1][y + 1].get_color() != color):
            return True

        # Check down 1 (x + 1)
        if (x < 7 and self.chessArray[x + 1][y] != None and self.chessArray[x + 1][y].get_name() == "k" and self.chessArray[x + 1][y].get_color() != color):
            return True
        # Check down 1, left 1 (x + 1, y - 1)
        if (x < 7 and y > 0 and self.chessArray[x + 1][y - 1] != None and self.chessArray[x + 1][y - 1].get_name() == "k" and self.chessArray[x + 1][y - 1].get_color() != color):
            return True

        # Check left 1 (y - 1)
        if (y > 0 and self.chessArray[x][y - 1] != None and self.chessArray[x][y - 1].get_name() == "k" and self.chessArray[x][y - 1].get_color() != color):
            return True
        # Check up 1, left 1 (x - 1, y -  1)
        if (x > 0 and y > 0 and self.chessArray[x - 1][y - 1] != None and self.chessArray[x - 1][y - 1].get_name() == "k" and self.chessArray[x - 1][y - 1].get_color() != color):
            return True
        return False

    # Iterates through each white piece location and updates the pieces with the new available moves. 
    def whitePieceUpdate(self):
        for x, y in self.whitePieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check. Since pawns can move only one way, they don't have a function. 
                possibleMoves = self.pawnCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "r"): # Rook
                possibleMoves = self.rookCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "b"): # Bishop
                possibleMoves = self.bishopCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "q"): # Queen (moves both diagonally and orthogonally)
                possibleMoves = self.rookCheck(x, y, "white")
                possibleMoves.extend(self.bishopCheck(x, y, "white"))
            elif (self.chessArray[x][y].get_name() == "kn"): # Knight
                possibleMoves = self.knightCheck(x, y, "white")
            elif (self.chessArray[x][y].get_name() == "k"): # King
                possibleMoves = self.kingCheck(x, y, "white")
                self.whiteKingXY = (x, y)
            print("WHITE {} AT ({}, {}). It can move to ".format(self.getSquare(x, y).get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves) # Updates the moves of the piece. 

    # Same as whitePieceCheck, but for the black pieces. 
    def blackPieceUpdate(self):
        for x, y in self.blackPieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                possibleMoves = self.pawnCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "r"):
                possibleMoves = self.rookCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "b"):
                possibleMoves = self.bishopCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "q"): # maybe..?
                possibleMoves = self.rookCheck(x, y, "black")
                possibleMoves.extend(self.bishopCheck(x, y, "black"))
            elif (self.chessArray[x][y].get_name() == "kn"):
                possibleMoves = self.knightCheck(x, y, "black")
            elif (self.chessArray[x][y].get_name() == "k"): 
                possibleMoves = self.kingCheck(x, y, "black")
                self.blackKingXY = (x, y)
            print("BLACK {} AT ({}, {}). It can move to ".format(self.chessArray[x][y].get_name(), x, y), end="")
            print(possibleMoves)
            self.chessArray[x][y].updatePossibleMoves(possibleMoves)
    
    # Can the square at (x, y) be captured by the opposing color pieces?
    # Returns True if so and False if not. 
    # Use this to check for check with the stored kingXY values. 
    def captureCheck(self, x, y, color):
        oppPieces = None
        if (color == "white"):
            oppPieces = self.blackPieces
        else:
            oppPieces = self.whitePieces
        
        for x2, y2 in oppPieces:
            piece = self.chessArray[x2][y2].get_possible_moves()
            if ((x, y) in piece):
                return True
        return False
    
    # Assumptions: There is a {color} king at the stored XY location. This king is in check. 
    # Checks if the king is in checkmate. 
    def checkmateCheck(self, color): 
        if (color == "white"):
            x, y = self.whiteKingXY
        elif (color == "black"):
            x, y = self.blackKingXY
        else:
            print("invalid color")
            return False
        print(x, y)
        capturingPieces, involvedSquares = self.lineOfSight(x, y, color)

        # How many pieces can capture the king?
        if (len(capturingPieces) < 1): # No piece can capture the king. 
            return False # Not checkmate. 
        elif (len(capturingPieces) > 1): # Multiple pieces can capture the king.
            return True # Checkmate.
        
        # There is only one capturing piece and the involvedPieces list is all the squares in between. 
        # Test all possible moves for check. 
        noKing = self.copy_board()
        noKing.__clearSquare(x, y) # Remove the king so it does not block it's own line of sight. 
        for x1, y1 in self.chessArray[x][y].get_possible_moves():
            res = noKing.lineOfSight(x1, y1, color)
            if (len(res[0]) == 0): # If the king can move somewhere, it is not in checkmate.
                return False
        
        if (color == "white"):
            allPieces = self.whitePieces
        else:
            allPieces = self.blackPieces
        allPieces.remove((x, y)) # Do not include the king!

        for coords in involvedSquares: # For each involved square in the 
            for x2, y2 in allPieces:
                if (coords in self.chessArray[x2][y2].get_possible_moves()):
                    return False
        print(capturingPieces, involvedSquares)
        return True

    # From the the current square, what can capture that square?
    # Iterates through each possible location and returns a tuple. 
    # (List of pieces that can capture the square, List of all squares involved in the line of sight)
    def lineOfSight(self, x, y, color): 
        # print("LINEOFSIGHT:")
        capturingPieces = []
        involvedSquares = []

        # Knights can skip over squares, so the only thing to check is each knight square. 
        for a, b in self.knightCheck(x, y, color)[0]:
            if (self.chessArray[a][b] != None and self.chessArray[a][b].get_name() == "kn"):
                capturingPieces.append((a, b))
                involvedSquares.append((a, b))

        for a in self.rookCheck(x, y, color):
            if (len(a) == 0):
                continue
            piece = self.getSquare(a[-1][0], a[-1][1])
            if (piece != None and piece.get_color() != color):
                if (piece.get_name() == "r" or piece.get_name() == "q"):
                    capturingPieces.append(a[-1])
                    involvedSquares.extend(a)

        for a in self.bishopCheck(x, y, color):
            if (len(a) == 0):
                continue
            piece = self.getSquare(a[-1][0], a[-1][1])
            if (piece != None and piece.get_color() != color and (piece.get_name() == "b" or piece.get_name() == "q")):
                    capturingPieces.append(a[-1])
                    involvedSquares.extend(a)

        for b in self.pawnCheck(x, y, color)[1]: 
            # Only the capture movements!
            # b is an (x, y) tuple. 
            piece = self.getSquare(b[0], b[1]) 
            if (piece != None and piece.get_color() != color and piece.get_name() == "p"):
                capturingPieces.append(b)
                involvedSquares.append(b)
        return (capturingPieces, involvedSquares)
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
    b.addPiece(0, 3, "k", "black") # PossibleMoves = None
    b.addPiece(1, 5, "k", "white")
    b.addPiece(7, 5, "r", "black")
    b.addPiece(3, 0, "b", "white")
    b.addPiece(2, 2, "kn", "white")
    b.addPiece(0, 6, "p", "black")
    b.addPiece(0, 4, "p", "black")
    b.addPiece(2, 4, "p", "black")
    b.addPiece(1, 4, "q", "black")
    b.addPiece(0, 5, "q", "white")

def CheckMateState(b):
    b.clear()
    b.addPiece(3, 3, "k", "black")
    b.addPiece(3, 0, "r", "white")
    b.addPiece(2, 6, "r", "white")
    b.addPiece(5, 1, "p", "white")
    b.addPiece(5, 5, "kn", "white")
    b.addPiece(7, 1, "b", "white")

    b.addPiece(0, 1, "r", "black")

def main():
    newgame = board()
    CheckMateState(newgame)
    newgame.printBoardState()
    newgame.whitePieceUpdate()
    newgame.blackPieceUpdate()
    print(newgame.checkmateCheck("black"))
    # print(newgame.lineOfSight(1, 5, "white"))

    # game2 = board(newgame)
    # newgame.printBoardState()


main()