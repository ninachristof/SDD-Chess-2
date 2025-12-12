import pygame
import modifiers

class chesspiece:
    name = None
    x = 0
    y = 0
    color = None
    first_move = True

    possible_capture = []
    possible_non_capture = []
    possible_moves = [] #These are all moves that don't go off the board
    legal_moves = [] #These are all possible_moves that also (1) don't require going through pieces and (2) don't leave the king in check
    multiple_moves = False
    capture_only_with_piece = False
    sprite = None
    upgrades = [[],[]]
    upgrade = None
    debuff = None

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.upgrades = [[],[]]
        self.is_upgraded = False
        self.upgrade = None
        self.debuff = None

    def get_is_upgraded(self):
        return not(len(self.upgrades[0]) == 0 and len(self.upgrades[1]) == 0)
    
    def get_is_debuffed(self):
        return not(self.debuff == None)

    #def get_upgrades(self):
    #    return upgrades
    
    def set_upgrade(self,upgrade):
        self.upgrade = upgrade
    
    def set_debuff(self,debuff):
        self.debuff = debuff

    def update_coordinates(self,x,y):
        self.x = x
        self.y = y

    def apply_debuff(self,moveset):
        print("Applying debuffs for ", self.x, self.y)
        return modifiers.apply_debuff(self.x,self.y,moveset,self.debuff.get_id())

    def get_upgrade_desc(self):
        return self.upgrade.get_description()
    
    def get_debuff_desc(self):
        return self.debuff.get_description()
    
    def get_name(self): 
        return self.name
    
    def get_color(self):
        return self.color
    
    def has_moved(self):
        return self.first_move
    
    def get_spite(self):
        return self.sprite
    
    def get_possible_capture(self):
        moves = self.possible_capture.copy()
        return self.possible_capture.copy()

    def get_possible_noncapture(self):
        return self.possible_non_capture.copy()
    
    # Takes in a list of lists of possible New moves, split into subgroups. 
    # Unfolds that list of lists. 
    def update_possible_moves(self, newMoves):
        self.possible_moves = []
        for subList in newMoves:
            self.possible_moves.extend([subList])

    def update_legal_moves(self,newMoves):
        self.legal_moves = []
        for subList in newMoves:
            self.legal_moves.extend([subList])

    def get_possible_moves(self):
        return self.possible_moves.copy()
    
    def get_legal_moves(self):
        return self.legal_moves.copy()
        
    def get_capture_only_with_piece(self):
        return self.capture_only_with_piece

    def set_first_move(self):
        self.first_move = False

    def find_moves(self, x, y):
        possible_capture,possible_moves = self.upgrades
        filtered_capture = []
        filtered_moves = []
        if (len(possible_capture) > 0):
            for LOS in possible_capture:
                filtered_LOS = []
                if (len(LOS) == 0):
                    continue
                for (dx,dy) in LOS:
                    if (x + dx < 8 and x + dx >= 0 and y + dy < 8 and y + dy >= 0):
                        filtered_LOS.append((x+dx,y+dy))
                    else:
                        break
                filtered_capture.append(filtered_LOS)

        if (len(possible_moves) > 0):
            for LOS in possible_moves:
                filtered_LOS = []
                if (len(LOS) == 0):
                    continue
                for (dx,dy) in LOS:
                    if (x + dx < 8 and x + dx >= 0 and y + dy < 8 and y + dy >= 0):
                        filtered_LOS.append((x+dx,y+dy))
                    else:
                        break
                filtered_moves.append(filtered_LOS)
        return filtered_capture,filtered_moves
        

class pawn(chesspiece):
    def __init__(self,x,y,color):
        #self.multiple_moves = True
        #needs initial [2,0] move
        super().__init__(x,y,color)
        self.name = "p"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_plt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_pdt60.png"), (80,80))
        self.find_moves(x,y)
        
        self.capture_only_with_piece = True
    
    def find_moves(self, x, y):
        powerup_capture, powerup_move = super().find_moves(x,y)
        possible_noncapture = []
        possible_capture = []
        # Forwards movement
        if (self.color == "white"):
            if (x > 0):
                possible_noncapture.append((x - 1, y))
                if (x != 1 and self.first_move):
                    possible_noncapture.append((x - 2, y))
            # Capture Movement
            if (x > 0 and y > 0):
                possible_capture.append([(x - 1, y - 1)])
            if (x > 0 and y < 7):
                possible_capture.append([(x - 1, y + 1)])
                print(2,possible_capture[-1])
        else:
            if (x < 7):
                possible_noncapture.append((x + 1, y))
                if (x < 6 and self.first_move):
                    possible_noncapture.append((x + 2, y))
            # Capture Movement
            if (x < 7 and y > 0):
                possible_capture.append([(x + 1, y - 1)])
            if (x < 7 and y < 7): 
                possible_capture.append([(x + 1, y + 1)])
        # possible_capture = [possible_capture]
        possible_noncapture = [possible_noncapture]
        possible_capture.extend(powerup_capture)
        possible_noncapture.extend(powerup_move)
        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        #print("Find moves gives ", possible_noncapture, possible_capture)
        return (possible_noncapture, possible_capture)


class knight(chesspiece):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.name = "kn"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_nlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_ndt60.png"), (80,80))
        self.find_moves(x,y)

    def find_moves(self, x, y):
        powerup_capture,powerup_move = super().find_moves(x,y)
        possible_noncapture = []
        possible_capture = []

        if (x > 1 and y < 7):
            possible_capture.append([(x - 2, y + 1)])
        # Move up1, right 2 (x - 1, y + 2)
        if (x > 0 and y < 6):
            possible_capture.append([(x - 1, y + 2)])

        # Move down1, right 2 (x + 1, y + 2)
        if (x < 7 and y < 6):
            possible_capture.append([(x + 1, y + 2)])
        # Move down2, right 1 (x + 2, y + 1)
        if (x < 6 and y < 7):
            possible_capture.append([(x + 2, y + 1)])

        # Move down 2, left 1 (x + 2, y - 1)
        if (x < 6 and y > 0):
            possible_capture.append([(x + 2, y - 1)])
        # Move down 1, left 2 (x + 1, y - 2)
        if (x < 7 and y > 1):
            possible_capture.append([(x + 1,y - 2)])

        # Move up 1, left 2 (x - 1, y - 2)
        if (x > 0 and y > 1):
            possible_capture.append([(x - 1, y - 2)])
        # Move up 2, left 1 (x - 2, y -  1)
        if (x > 1 and y > 0):
            possible_capture.append([(x - 2,y - 1)])
        possible_capture.extend(powerup_capture)
        possible_noncapture.extend(powerup_move)

        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        #print("Find moves gives ", possible_noncapture, possible_capture)
        return (possible_noncapture, possible_capture)

class king(chesspiece):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.name = "k"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_klt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_kdt60.png"), (80,80))
        self.find_moves(x,y)
        

    def find_moves(self, x, y):
        powerup_capture,powerup_move = super().find_moves(x,y)
        possible_noncapture = []
        possible_capture = []
        if (x > 0):
            possible_capture.append([(x - 1, y)])
        # Move up 1, right 1 (x - 1, y + 1)
        if (x > 0 and y < 7):
            possible_capture.append([(x - 1, y + 1)])

        # Move right 1 (y + 1)
        if (y < 7):
            possible_capture.append([(x, y + 1)])
        # Move down 1, right 1 (x + 1, y + 1)
        if (x < 7 and y < 7):
            possible_capture.append([(x + 1, y + 1)])

        # Move down 1 (x + 1)
        if (x < 7):
            possible_capture.append([(x + 1, y)])
        # Move down 1, left 1 (x + 1, y - 1)
        if (x < 7 and y > 0):
            possible_capture.append([(x + 1,y - 1)])

        # Move left 1 (y - 1)
        if (y > 0):
            possible_capture.append([(x, y - 1)])
        # Move up 1, left 1 (x - 1, y -  1)
        if (x > 0 and y > 0):
            possible_capture.append([(x - 1,y - 1)])
        #print("Find moves gives ", possible_noncapture, possible_capture)

        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        return (possible_noncapture, possible_capture)

class rook(chesspiece):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.name = "r"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_rlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_rdt60.png"), (80,80))
        self.find_moves(x,y)
        
    def find_moves(self, x, y):
        powerup_capture,powerup_move = super().find_moves(x,y)
        possible_noncapture = [[]]

        possible_up = []
        # Check move upwards (x - 1)
        iter = x - 1
        while (iter >= 0):
            # While the iter is still on the board AND the square is empty...
            possible_up.append((iter, y)) # Add the square to the possible moves. 
            iter -= 1 # Move up. 

        possible_right = []
        iter = y + 1
        # Check move right (y + 1)
        while (iter <= 7):
            possible_right.append((x, iter))
            iter += 1

        possible_down = []
        iter = x + 1
        # Check move downwards (x + 1)
        while (iter <= 7):
            possible_down.append((iter, y))
            iter += 1
        
        possible_left = []
        iter = y - 1
        # Check move left (y - 1)
        while (iter >= 0):
            possible_left.append((x, iter))
            iter -= 1

        possible_noncapture.extend(powerup_move)
        possible_capture = [possible_up, possible_right, possible_down, possible_left]
        possible_capture.extend(powerup_capture)

        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        #print("Find moves gives ", possible_noncapture, possible_capture)
        return (possible_noncapture, possible_capture)

class bishop(chesspiece):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.name = "b"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_blt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_bdt60.png"), (80,80))
        self.find_moves(x,y)

    def find_moves(self, x, y):
        powerup_capture,powerup_move = super().find_moves(x,y)
        possible_noncapture = [[]]

        possible_upRight = []
        iter = x - 1
        iter2 = y + 1
        # Check move up-right (x - 1, y + 1)
        while (iter >= 0 and iter2 <= 7):
            possible_upRight.append((iter, iter2))
            iter -= 1
            iter2 += 1

        possible_downRight = []
        iter = x + 1
        iter2 = y + 1
        # Check move down-right (x + 1, y + 1)
        while (iter <= 7 and iter2 <= 7):
            possible_downRight.append((iter, iter2))
            iter += 1
            iter2 += 1

        possible_downLeft = []
        iter = x + 1
        iter2 = y - 1
        # Check move down-left (x + 1, y - 1)        
        while (iter <= 7 and iter2 >= 0):
            possible_downLeft.append((iter, iter2))
            iter += 1
            iter2 -= 1

        possible_upLeft = []
        iter = x - 1
        iter2 = y - 1
        # Check move up-left (x - 1, y - 1)
        while (iter >= 0 and iter2 >= 0):
            possible_upLeft.append((iter, iter2))
            iter -= 1
            iter2 -= 1
        
        possible_noncapture.extend(powerup_move)
        possible_capture = [possible_upRight, possible_downRight, possible_downLeft, possible_upLeft]
        possible_capture.extend(powerup_capture)

        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        #print("Find moves gives ", possible_noncapture, possible_capture)
        return (possible_noncapture, possible_capture)

class queen(bishop, rook):
    def __init__(self,x,y,color):
        super().__init__(x,y,color)
        self.name = "q"
        if(color == "white"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_qlt60.png"), (80,80))
        elif(color == "black"):
            self.sprite = pygame.transform.scale(pygame.image.load("resources/Chess_qdt60.png"), (80,80))
        self.find_moves(x,y)

    def find_moves(self, x, y):
        powerup_capture, powerup_move = super().find_moves(x,y)
        possible_noncapture = [[]]
        possible_capture = []
        b1, b2 = bishop.find_moves(bishop(x, y, self.color), x, y)
        r1, r2 = rook.find_moves(rook(x, y, self.color), x, y)

        possible_noncapture.extend(powerup_move)
        possible_noncapture.extend(b1)
        possible_noncapture.extend(r1)

        possible_capture.extend(powerup_capture)
        possible_capture.extend(b2)
        possible_capture.extend(r2)

        self.possible_capture = possible_capture
        self.possible_non_capture = possible_noncapture
        #print("Find moves gives ", possible_noncapture, possible_capture)
        return (possible_noncapture, possible_capture)
