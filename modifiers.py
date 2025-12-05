from powerup import *
from debuff import *
import random

pawnPowerUps= [
    powerup(" can move backwards one square",[],[[(-1,0)],[(1,0)]])
]
knightPowerUps = [
    powerup(" can move one square along a row or column", [],[[(-1,0)],[(1,0)],[(0,1)],[(0,-1)]])
]

bishopPowerUps = [
    powerup(" can move one square along a row or column", [],[[(-1,0)],[(1,0)],[(0,1)],[(0,-1)]])
]
rookPowerUps = [
    powerup(" can move one square diagonally", [],[[(-1,-1)],[(1,1)],[(-1,1)],[(1,-1)]])
]
queenPowerUps = [
    powerup(" can move like a knight", [], [[(-2,-1)],[(2,1)],[(-2,1)],[(2,-1)],[(-1,-2)],[(1,2)],[(-1,2)],[(1,-2)]])
]

kingPowerUps = [
    powerup(" can capture pieces two squares away along a row or column #WIP", [[(-1,0),(-2,0)],[(1,0),(2,0)],[(0,1),(0,2)],[(0,-1),(0,-2)]], [])
]

lookup = {
    "p":pawnPowerUps,
    "kn":knightPowerUps,
    "b":bishopPowerUps,
    "r":rookPowerUps,
    "q":queenPowerUps,
    "k":kingPowerUps
}

debuffs = [
    debuff(" can move a Euclidean Distance of at most 5", 0),
    debuff(" can't move more than 3 rows or columns from current position ", 1)
]

#temp fix:
debuff_map = {
    0 : debuffs[0],
    1 : debuffs[1]
}

def apply_debuff(x,y,moveset,id):
    new_moveset = []
    if (id == 0):
        for move in moveset:
            if (abs(x-move[0]) + abs(y-move[1]) <= 6):
                new_moveset.append(move)
            # else:
            #     print("Filtered out ", move)
    if (id == 1):
        for move in moveset:
            if (not(abs(x-move[0]) > 4 and abs(y-move[1]) > 4)):
                new_moveset.append(move)
            # else:
            #     print("Filtered out ", move)
    return new_moveset

def getPowerups(piecename):
    return lookup[piecename][0]

def getDebuff():
    #print("Debuffing!")
    return debuffs[random.randint(0,len(debuffs)-1)]
