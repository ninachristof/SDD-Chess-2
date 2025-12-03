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
    powerup(" can move like a knight", [], [])
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
    debuff(" can move a Euclidean Distance of at most 6", 0),
    debuff(" can't move more than 2 rows or columns from current position ", 1),
    debuff(" can only move during odd turns", 2)
]

def getPowerups(piecename):
    return lookup[piecename][0]

def getDebuff():
    print("Debuffing!")
    return debuffs[random.randint(0,2)]