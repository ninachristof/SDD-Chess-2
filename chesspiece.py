import pygame

class chesspiece:
    name = None
    x = 0
    y = 0
    color = None
    firstMove = True

    possible_Capture = []
    possible_NonCapture = []
    possibleMoves = [] #These are all moves that don't go off the board
    legalMoves = [] #These are all possibleMoves that also (1) don't require going through pieces and (2) don't leave the king in check
    multipleMoves = False
    captureOnlyWithPiece = False
    sprite = None
    upgrades = [[],[]]
    
    def get_name(self): 
        return self.name
    
    def get_color(self):
        return self.color
    
    def hasMoved(self):
        return self.firstMove
    
    def get_spite(self):
        return self.sprite
    
    def getPossibleCapture(self):
        return self.possible_Capture.copy()

    def getPossibleNoncapture(self):
        return self.possible_NonCapture.copy()
    
    # Takes in a list of lists of possible New moves, split into subgroups. 
    # Unfolds that list of lists. 
    def updatePossibleMoves(self, newMoves):
        self.possibleMoves = []
        for subList in newMoves:
            self.possibleMoves.extend([subList])

    def updateLegalMoves(self,newMoves):
        self.legalMoves = []
        for subList in newMoves:
            self.legalMoves.extend([subList])

    def get_possible_moves(self):
        return self.possibleMoves.copy()
    
    def getlegalMoves(self):
        return self.legalMoves.copy()
        
    def get_captureOnlyWithPiece(self):
        return self.captureOnlyWithPiece

    def set_first_move(self):
        self.firstMove = False

    def findMoves(self, x, y):
        possibleCapture,possibleMoves = self.upgrades
        filteredCapture = []
        filteredMoves = []
        if (len(possibleCapture) > 0):
            for LOS in possibleCapture:
                filteredLOS = []
                if (len(LOS) == 0):
                    continue
                for (dx,dy) in LOS:
                    if (x + dx < 8 and x + dx >= 0 and y + dy < 8 and y + dy >= 0):
                        filteredLOS.append((x+dx,y+dy))
                    else:
                        break
                filteredCapture.append(filteredLOS)

        if (len(possibleMoves) > 0):
            for LOS in possibleMoves:
                filteredLOS = []
                if (len(LOS) == 0):
                    continue
                for (dx,dy) in LOS:
                    if (x + dx < 8 and x + dx >= 0 and y + dy < 8 and y + dy >= 0):
                        filteredLOS.append((x+dx,y+dy))
                    else:
                        break
                filteredMoves.append(filteredLOS)
        return filteredCapture,filteredMoves
        

class pawn(chesspiece):
    def __init__(self,x,y,color):
        #self.multipleMoves = True
        #needs initial [2,0] move
        self.name = "p"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_plt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_pdt60.png"), (80,80))
        self.findMoves(x,y)
        
        self.captureOnlyWithPiece = True
    
    def findMoves(self, x, y):
        powerupCapture, powerupMove = super().findMoves(x,y)
        possibleNoncapture = []
        possibleCapture = []
        # Forwards movement
        if (self.color == "white"):
            if (x != 0):
                possibleNoncapture.append((x - 1, y))
                if (x != 1 and self.firstMove):
                    possibleNoncapture.append((x - 2, y))
            # Capture Movement
            if (x != 0 and y != 0):
                possibleCapture.append([(x - 1, y - 1)])
            if (x != 0 and y != 7):
                possibleCapture.append([(x - 1, y + 1)])
        else:
            if (x != 7):
                possibleNoncapture.append((x + 1, y))
                if (x != 6 and self.firstMove):
                    possibleNoncapture.append((x + 2, y))
            # Capture Movement
            if (x != 7 and y != 0):
                possibleCapture.append([(x + 1, y - 1)])
            if (x != 6 and y != 7): 
                possibleCapture.append([(x + 1, y + 1)])
        # possibleCapture = [possibleCapture]
        possibleNoncapture = [possibleNoncapture]
        possibleCapture.extend(powerupCapture)
        possibleNoncapture.extend(powerupMove)
        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        #print("Find moves gives ", possibleNoncapture, possibleCapture)
        return (possibleNoncapture, possibleCapture)


class knight(chesspiece):
    def __init__(self,x,y,color):
        self.name = "kn"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_nlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_ndt60.png"), (80,80))
        self.findMoves(x,y)

    def findMoves(self, x, y):
        powerupCapture,powerupMove = super().findMoves(x,y)
        possibleNoncapture = []
        possibleCapture = []

        if (x > 1 and y < 7):
            possibleCapture.append([(x - 2, y + 1)])
        # Move up1, right 2 (x - 1, y + 2)
        if (x > 0 and y < 6):
            possibleCapture.append([(x - 1, y + 2)])

        # Move down1, right 2 (x + 1, y + 2)
        if (x < 7 and y < 6):
            possibleCapture.append([(x + 1, y + 2)])
        # Move down2, right 1 (x + 2, y + 1)
        if (x < 6 and y < 7):
            possibleCapture.append([(x + 2, y + 1)])

        # Move down 2, left 1 (x + 2, y - 1)
        if (x < 6 and y > 0):
            possibleCapture.append([(x + 2, y - 1)])
        # Move down 1, left 2 (x + 1, y - 2)
        if (x < 7 and y > 1):
            possibleCapture.append([(x + 1,y - 2)])

        # Move up 1, left 2 (x - 1, y - 2)
        if (x > 0 and y > 1):
            possibleCapture.append([(x - 1, y - 2)])
        # Move up 2, left 1 (x - 2, y -  1)
        if (x > 1 and y > 0):
            possibleCapture.append([(x - 2,y - 1)])
        possibleCapture.extend(powerupCapture)
        possibleNoncapture.extend(powerupMove)

        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        #print("Find moves gives ", possibleNoncapture, possibleCapture)
        return (possibleNoncapture, possibleCapture)

class king(chesspiece):
    def __init__(self,x,y,color):
        self.name = "k"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_klt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_kdt60.png"), (80,80))
        self.findMoves(x,y)
        

    def findMoves(self, x, y):
        powerupCapture,powerupMove = super().findMoves(x,y)
        possibleNoncapture = []
        possibleCapture = []
        if (x > 0):
            possibleCapture.append([(x - 1, y)])
        # Move up 1, right 1 (x - 1, y + 1)
        if (x > 0 and y < 7):
            possibleCapture.append([(x - 1, y + 1)])

        # Move right 1 (y + 1)
        if (y < 7):
            possibleCapture.append([(x, y + 1)])
        # Move down 1, right 1 (x + 1, y + 1)
        if (x < 7 and y < 7):
            possibleCapture.append([(x + 1, y + 1)])

        # Move down 1 (x + 1)
        if (x < 7):
            possibleCapture.append([(x + 1, y)])
        # Move down 1, left 1 (x + 1, y - 1)
        if (x < 7 and y > 0):
            possibleCapture.append([(x + 1,y - 1)])

        # Move left 1 (y - 1)
        if (y > 0):
            possibleCapture.append([(x, y - 1)])
        # Move up 1, left 1 (x - 1, y -  1)
        if (x > 0 and y > 0):
            possibleCapture.append([(x - 1,y - 1)])
        #print("Find moves gives ", possibleNoncapture, possibleCapture)

        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        return (possibleNoncapture, possibleCapture)

class rook(chesspiece):
    def __init__(self,x,y,color):
        self.name = "r"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_rlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_rdt60.png"), (80,80))
        self.findMoves(x,y)
        
    def findMoves(self, x, y):
        powerupCapture,powerupMove = super().findMoves(x,y)
        possibleNoncapture = [[]]

        possibleUp = []
        # Check move upwards (x - 1)
        iter = x - 1
        while (iter >= 0):
            # While the iter is still on the board AND the square is empty...
            possibleUp.append((iter, y)) # Add the square to the possible moves. 
            iter -= 1 # Move up. 

        possibleRight = []
        iter = y + 1
        # Check move right (y + 1)
        while (iter <= 7):
            possibleRight.append((x, iter))
            iter += 1

        possibleDown = []
        iter = x + 1
        # Check move downwards (x + 1)
        while (iter <= 7):
            possibleDown.append((iter, y))
            iter += 1
        
        possibleLeft = []
        iter = y - 1
        # Check move left (y - 1)
        while (iter >= 0):
            possibleLeft.append((x, iter))
            iter -= 1

        possibleNoncapture.extend(powerupMove)
        possibleCapture = [possibleUp, possibleRight, possibleDown, possibleLeft]
        possibleCapture.extend(powerupCapture)

        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        #print("Find moves gives ", possibleNoncapture, possibleCapture)
        return (possibleNoncapture, possibleCapture)

class bishop(chesspiece):
    def __init__(self,x,y,color):
        self.name = "b"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_blt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_bdt60.png"), (80,80))
        self.findMoves(x,y)

    def findMoves(self, x, y):
        powerupCapture,powerupMove = super().findMoves(x,y)
        possibleNoncapture = [[]]

        possibleUpRight = []
        iter = x - 1
        iter2 = y + 1
        # Check move up-right (x - 1, y + 1)
        while (iter >= 0 and iter2 <= 7):
            possibleUpRight.append((iter, iter2))
            iter -= 1
            iter2 += 1

        possibleDownRight = []
        iter = x + 1
        iter2 = y + 1
        # Check move down-right (x + 1, y + 1)
        while (iter <= 7 and iter2 <= 7):
            possibleDownRight.append((iter, iter2))
            iter += 1
            iter2 += 1

        possibleDownLeft = []
        iter = x + 1
        iter2 = y - 1
        # Check move down-left (x + 1, y - 1)        
        while (iter <= 7 and iter2 >= 0):
            possibleDownLeft.append((iter, iter2))
            iter += 1
            iter2 -= 1

        possibleUpLeft = []
        iter = x - 1
        iter2 = y - 1
        # Check move up-left (x - 1, y - 1)
        while (iter >= 0 and iter2 >= 0):
            possibleUpLeft.append((iter, iter2))
            iter -= 1
            iter2 -= 1
        
        possibleNoncapture.extend(powerupMove)
        possibleCapture = [possibleUpRight, possibleDownRight, possibleDownLeft, possibleUpLeft]
        possibleCapture.extend(powerupCapture)

        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        #print("Find moves gives ", possibleNoncapture, possibleCapture)
        return (possibleNoncapture, possibleCapture)

class queen(bishop, rook):
    def __init__(self,x,y,color):
        self.name = "q"
        self.x = x
        self.y = y
        self.color = color
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_qlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_qdt60.png"), (80,80))
        self.findMoves(x,y)

    def findMoves(self, x, y):
        powerupCapture, powerupMove = super().findMoves(x,y)
        possibleNoncapture = [[]]
        possibleCapture = []
        b1, b2 = bishop.findMoves(bishop(x, y, self.color), x, y)
        r1, r2 = rook.findMoves(rook(x, y, self.color), x, y)

        possibleNoncapture.extend(powerupMove)
        possibleCapture.extend(powerupCapture)
        possibleNoncapture.extend(b1)
        possibleNoncapture.extend(r1)

        possibleCapture.extend(b2)
        possibleCapture.extend(r2)

        self.possible_Capture = possibleCapture
        self.possible_NonCapture = possibleNoncapture
        #print("Find moves gives ", possibleNoncapture, possibleCapture)
        return (possibleNoncapture, possibleCapture)
