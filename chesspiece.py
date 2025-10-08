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
    
    def get_firstMove(self):
        return self.firstMove
    
    def updatePossibleMoves(self, newMoves):
        self.possibleMoves = newMoves

    def get_possible_moves(self):
        return self.possibleMoves
        
    def set_first_move(self):
        self.firstMove = False

class pawn(chesspiece):
    def __init__(self,x,y,color):
        self.multipleMoves = True
        self.name = "p"
        self.x = x
        self.y = y
        self.color = color
        

class knight(chesspiece):
    def __init__(self,x,y,color):
        self.name = "kn"
        self.x = x
        self.y = y
        # self.possibleMoves = [
        #     [1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],
        #     [-2,1],[-2,-1]
        # ]
        self.image = "blackknight.png"
        self.color = color

class king(chesspiece):
    def __init__(self,x,y,color):
        self.name = "k"
        self.x = x
        self.y = y
        # self.possibleMoves = [[1,0]]
        self.color = color

class queen(chesspiece):
    def __init__(self,x,y,color):
        self.name = "q"
        self.x = x
        self.y = y
        # self.possibleMoves = [[1,0]]
        self.color = color

class rook(chesspiece):
    def __init__(self,x,y,color):
        self.name = "r"
        self.x = x
        self.y = y
        # self.possibleMoves = [[1,0]]
        self.color = color

class bishop(chesspiece):
    def __init__(self,x,y,color):
        self.name = "b"
        self.x = x
        self.y = y
        # self.possibleMoves = [[1,0]]
        self.color = color