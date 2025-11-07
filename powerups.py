from powerup import *
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
    powerup(" gains knight movement #WIP", [], [])
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

def getPowerups(piecename):
    return lookup[piecename][0]