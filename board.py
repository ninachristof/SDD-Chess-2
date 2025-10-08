from chesspiece import *

class board:
    chessArray = [[None for j in range(8)] for i in range(8)]
    whitePieces = []
    blackPieces = []

    def __init__(self): # Initial board setup. 
        # Initialize Pawns
        for i in range(8):
            self.chessArray[1][i] = pawn(1,i,"black")
            self.chessArray[6][i] = pawn(6,i,"white")
            self.whitePieces.append((6, i))
            self.blackPieces.append((1, i))
            
        # Initialize Knights
        self.chessArray[7][1] = knight(7,1,"white")
        self.chessArray[7][6] = knight(7,6,"white")
        self.chessArray[0][1] = knight(0,1,"black")
        self.chessArray[0][6] = knight(0,6,"black")
        self.whitePieces.append((7, 1))
        self.whitePieces.append((7, 6))
        self.blackPieces.append((0, 1))
        self.blackPieces.append((0, 6))
        
        # Initialize Rooks
        self.chessArray[7][0] = rook(7,0,"white")
        self.chessArray[7][7] = rook(7,7,"white")
        self.chessArray[0][0] = rook(0,0,"black")
        self.chessArray[0][7] = rook(0,7,"black")
        self.whitePieces.append((7, 0))
        self.whitePieces.append((7, 7))
        self.blackPieces.append((0, 0))
        self.blackPieces.append((0, 7))

        # Initialize Bishops
        self.chessArray[7][2] = bishop(7,2,"white")
        self.chessArray[7][5] = bishop(7,5,"white")
        self.chessArray[0][2] = bishop(0,2,"black")
        self.chessArray[0][5] = bishop(0,5,"black")
        self.whitePieces.append((7, 2))
        self.whitePieces.append((7, 5))
        self.blackPieces.append((0, 2))
        self.blackPieces.append((0, 5))
        
        # Initialize Kings and Queens
        self.chessArray[7][4] = king(7,2,"white")
        self.chessArray[7][3] = queen(7,5,"white")
        self.chessArray[0][4] = king(0,2,"black")
        self.chessArray[0][3] = queen(0,5,"black")
        self.whitePieces.append((7, 4))
        self.whitePieces.append((7, 3))
        self.blackPieces.append((0, 4))
        self.blackPieces.append((0, 3))

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
    
    def knightCheck(self):
        return

    def whitePieceCheck(self):
        for x, y in self.whitePieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                possibleMoves.append((x - 1, y))
                if (self.chessArray[x][y].get_firstMove()):
                    possibleMoves.append((x - 2, y))
                print("PAWN AT {}, {}. It can move to ".format(x, y), end="")
                print(possibleMoves)
                for i in possibleMoves:
                    if (self.chessArray[i[0]][i[1]] != None):
                        possibleMoves.remove(i)
                self.chessArray[x][y].updatePossibleMoves(possibleMoves)
            elif (self.chessArray[x][y].get_name() == "r"):
                self.rookCheck()
            # print(self.chessArray[x][y].get_name() + " " + self.chessArray[x][y].get_color()[0] + " {0}, {1}".format(x, y))

    def blackPieceCheck(self):
        for x, y in self.blackPieces:
            possibleMoves = []
            if (self.chessArray[x][y].get_name() == "p"): # Pawn movement check.
                possibleMoves.append((x + 1, y))
                if (self.chessArray[x][y].get_firstMove()):
                    possibleMoves.append((x + 2, y))
                print("PAWN AT {}, {}. It can move to ".format(x, y), end="")
                print(possibleMoves)
            # print(self.chessArray[x][y].get_name() + " " + self.chessArray[x][y].get_color()[0] + " {0}, {1}".format(x, y))


'''
EN PASSANT CHECK: 
    Capturing en passant is permitted only on the turn *immediately* 
    after the two-square advance; it cannot be done on a later turn. 
This means that a pawn needs a boolean or something so it knows it moved twice. 
'''

def main():
    newgame = board()
    newgame.printBoardState()
    newgame.blackPieceCheck()
main()