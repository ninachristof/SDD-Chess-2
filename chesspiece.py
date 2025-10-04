class chesspiece:
    name = None
    x = 0
    y = 0
    image = None
    color = None
    firstMove = True
    firstPossibleMoves = None
    secondPossibleMoves = None
    multipleMoves = False
    
    def get_name(self): 
        return self.name
    
    def get_color(self):
        return self.color
    
    def get_possible_moves(self):
        # Check for pawns if you can move one or two spaces
        if(self.multipleMoves):
            if(self.firstMove):
                return self.firstPossibleMoves
            else: 
                return self.secondPossibleMoves
        else:
            return self.possiblemoves
        
    def set_first_move_true(self):
        self.firstMove = False
        return None
        
        

class pawn(chesspiece):
    def __init__(self,x,y,color):
        self.multipleMoves = True
        self.name = "p"
        self.x = x
        self.y = y
        self.firstPossibleMoves = [[1,0], [2,0]]
        self.secondPossibleMoves = [[1,0]]
        self.image = "blackpawn.png"
        self.color = color
        

class knight(chesspiece):
    def __init__(self,x,y,color):
        self.name = "kn"
        self.x = x
        self.y = y
        self.possiblemoves = [
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
        self.possiblemoves = [[1,0]]
        self.color = color

class queen(chesspiece):
    def __init__(self,x,y,color):
        self.name = "q"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]
        self.color = color

class rook(chesspiece):
    def __init__(self,x,y,color):
        self.name = "r"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]
        self.color = color

class bishop(chesspiece):
    def __init__(self,x,y,color):
        self.name = "b"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]
        self.color = color