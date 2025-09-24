class chesspiece:
    name = None
    x = 0
    y = 0
    image = None
    possiblemoves = None

class pawn(chesspiece):
    def __init__(self,x,y):
        self.name = "p"
        self.x = x
        self.y = y
        self.possiblemoves = [[0,1]]
        self.image = "blackpawn.png"

class knight(chesspiece):
    def __init__(self,x,y):
        self.name = "kn"
        self.x = x
        self.y = y
        self.possiblemoves = [
            [1,2],[1,-2],[2,1],[2,-1],[-1,2],[-1,-2],
            [-2,1],[-2,-1]
        ]
        self.image = "blackknight.png"

class king(chesspiece):
    def __init__(self,x,y):
        self.name = "k"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]

class queen(chesspiece):
    def __init__(self,x,y):
        self.name = "q"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]

class rook(chesspiece):
    def __init__(self,x,y):
        self.name = "r"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]

class bishop(chesspiece):
    def __init__(self,x,y):
        self.name = "b"
        self.x = x
        self.y = y
        self.possiblemoves = [[1,0]]