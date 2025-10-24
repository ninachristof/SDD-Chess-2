class chesspiece:
    name = None
    x = 0
    y = 0
    color = None
    firstMove = True
    possibleMoves = None
    multipleMoves = False
    
    def get_name(self): 
        return self.name
    
    def get_color(self):
        return self.color
    
    def hasMoved(self):
        return self.firstMove
    
    # Takes in a list of lists of possible New moves, split into subgroups. 
    # Unfolds that list of lists. 
    def updatePossibleMoves(self, newMoves):
        self.possibleMoves = []
        for subList in newMoves:
            self.possibleMoves.extend(subList)

    def get_possible_moves(self):
        return self.possibleMoves
        
    def set_first_move(self):
        self.firstMove = False

class pawn(chesspiece):
    def __init__(self,x,y,color):
        self.multipleMoves = True
        #needs initial [2,0] move
        self.possibleMoves = [[1,0]]
        self.name = "p"
        self.x = x
        self.y = y
        self.color = color
        

class knight(chesspiece):
    def __init__(self,x,y,color):
        self.name = "kn"
        self.x = x
        self.y = y
        self.possibleMoves = [
             [1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],
             [-2,1],[-2,-1]
        ]
        self.image = "blackknight.png"
        self.color = color

class king(chesspiece):
    def __init__(self,x,y,color):
        self.name = "k"
        self.x = x
        self.y = y
        self.possibleMoves = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
        self.color = color

class queen(chesspiece):
    def __init__(self,x,y,color):
        self.name = "q"
        self.x = x
        self.y = y
        self.possibleMoves = []
        for i in range(1, 8):
            self.possibleMoves.append([0,i])
            self.possibleMoves.append([0,-i])
            self.possibleMoves.append([i,0])
            self.possibleMoves.append([-i,0])
        for i in range(1, 8):
            self.possibleMoves.append([i,i])
            self.possibleMoves.append([-i,i])
            self.possibleMoves.append([i,-i])
            self.possibleMoves.append([-i,-i])
        self.color = color

class rook(chesspiece):
    def __init__(self,x,y,color):
        self.name = "r"
        self.x = x
        self.y = y
        self.possibleMoves = []
        for i in range(1, 8):
            self.possibleMoves.append([0,i])
            self.possibleMoves.append([0,-i])
            self.possibleMoves.append([i,0])
            self.possibleMoves.append([-i,0])
        self.color = color

class bishop(chesspiece):
    def __init__(self,x,y,color):
        self.name = "b"
        self.x = x
        self.y = y
        self.possibleMoves = []
        for i in range(1, 8):
            self.possibleMoves.append([i,i])
            self.possibleMoves.append([-i,i])
            self.possibleMoves.append([i,-i])
            self.possibleMoves.append([-i,-i])
        self.color = color
