from chesspiece import *
import time
import copy


class board:

    ##################################################################################
    ##################################################################################
    # EVERYTHING HERE IS PRIVATE
    # NOTHING OUTSIDE OF THE BOARD CLASS SHOULD BE CALLING THESE FUNCTIONS
    ##################################################################################
    ##################################################################################

    def __init__(self, initialize):
        # print("INITIALIZEING BOARD")
        self.chess_array = [[None for j in range(8)] for i in range(8)]
        self.white_pieces = []  # The list of locations for white pieces
        self.black_pieces = []  # The list of locations for black pieces
        self.en_passant_square = None   # For en passant check
        self.en_passant_pawn = None   # For en passant check

        # Automatically initialize start state
        if initialize:
            # print("Loading tester.txt")
            self.load_position("test_positions/start_state.txt")
            self.update_all_legal()

    def load_position(self, filepath):
        # Piece map for easier access
        piece_map = {
            'p': ("p", "black"),
            'r': ("r", "black"),
            'n': ("kn", "black"),
            'b': ("b", "black"),
            'q': ("q", "black"),
            'k': ("k", "black"),
            'P': ("p", "white"),
            'R': ("r", "white"),
            'N': ("kn", "white"),
            'B': ("b", "white"),
            'Q': ("q", "white"),
            'K': ("k", "white")
        }

        # Open file and split into lines
        with open(filepath, "r") as f:
            lines = f.read().splitlines()

        # Go through each line and add the piece to the board
        for i, row in enumerate(lines):
            for j, ch in enumerate(row):
                if ch == ".":
                    continue
                piece, color = piece_map[ch]
                self.add_piece(i, j, piece, color)

    def get_king_location(self, color):
        if (color == "white"):
            return self.white_king_xy
        if (color == "black"):
            return self.black_king_xy
        print("Invalid color")
        return (-1, -1)

    # Reset board and remove all pieces.

    def clear(self):
        self.chess_array = [[None for j in range(8)] for i in range(8)]
        self.white_pieces = []
        self.black_pieces = []

    def add_piece(self, x, y, piece, color):
        # The coordinates of this are a little messed up.
        # Current system: X is vertical going downwards, Y is horizontal going Right.

        # Valid coordinates check.
        if (x < 0 or x > 7 or y < 0 or y > 7):
            print(f"({x}, {y}) is not a valid coordinate.")
            return
        # Valid color check.
        if (color != "black" and color != "white"):
            print(f"{color} is not a valid color.")
            return

        # Empty square check.
        if (self.chess_array[x][y] != None):
            print(
                f"The {color} {piece} piece cannot be placed at ({x}, {y}) because there is already a {self.chess_array[x][y].get_color()} {self.chess_array[x][y].get_name()} piece there")
            return

        # Create a map of all the pieces for easier initialization
        piece_map = {
            "p": pawn,
            "kn": knight,
            "r": rook,
            "b": bishop,
            "q": queen,
            "k": king
        }

        if piece not in piece_map:
            print(f"Invalid piece name: {piece}")
            return

        # Create a the piece object using the map and place in correct spot
        piece_obj = piece_map[piece](x, y, color)
        self.chess_array[x][y] = piece_obj
        if color == "white":
            self.white_pieces.append((x, y))
            if piece == 'k':
                self.white_king_xy = (x, y)
        else:
            self.black_pieces.append((x, y))
            if piece == 'k':
                self.black_king_xy = (x, y)

    # Print the board.
    def printBoardState(self):
        print("  ", end="")
        for i in range(8):
            print(f"|  {i} ", end="")
        print("|")
        print("-" * 43)
        for i in range(8):
            print("{} |".format(i), end="")
            for j in range(8):
                if (self.chess_array[i][j] != None):
                    print("{0:4}".format(self.chess_array[i][j].get_name(
                    ) + " " + self.chess_array[i][j].get_color()[0]), end="|")
                else:
                    print("   ", end=" |")
            print("\n  " + "-" * 41)

    # Checks if the king that of the inputted color is in check
    def is_king_in_check(self, color):
        lookup = {"white": (self.white_king_xy, self.black_pieces),
                  "black": (self.black_king_xy, self.white_pieces)}
        kinglocation, enemypieces = lookup[color]
        for piece in enemypieces:
            x, y = piece[0], piece[1]
            color2 = self.chess_array[x][y].get_color()
            if kinglocation in self.get_possible_moves(x, y, color2):
                # print("King is in check by ", self.chess_array[x][y].get_color(),
                #        " " , self.chess_array[x][y].get_name(), " at " , x, ",", y)
                return True
        return False

    ##################################################################################
    ##################################################################################
    # Start of our public functions
    ##################################################################################
    ##################################################################################

    def get_square(self, i, j):
        if (i < 0 or j < 0 or i > 7 or j > 7):
            print("Not on board!")
            return None
        return self.chess_array[i][j]

    # Gets all possible moves (i.e. moves that aren't blocked by other pieces or don't send you off the board) subject to debuffs
    def get_possible_moves(self, x, y, color):
        possible_moves2 = []
        # print(self.chess_array[x][y].get_color()," ", self.chess_array[x][y].get_name(), " at ", x, "," , y)
        noncaptureMoves = self.chess_array[x][y].get_possible_noncapture()
        captureMoves = self.chess_array[x][y].get_possible_capture()

        # if (self.chess_array[x][y].get_name() == "q"):
        #     print (self.chess_array[x][y].get_color(), " ", self.chess_array[x][y].get_name())
        #     print("Noncapture moves: ", noncaptureMoves)
        #     print("Capture moves: ", captureMoves)
        # Line of sight check, stop if you hit a piece
        for direction in noncaptureMoves:
            for lineofsight in direction:
                if (self.chess_array[lineofsight[0]][lineofsight[1]] != None):
                    break
                possible_moves2.append(lineofsight)

        # print("PossibleMoves up to this point are ", possible_moves2)

        for direction in captureMoves:
            pieceFound = False
            temp = []
            for lineofsight in direction:
                if (self.chess_array[lineofsight[0]][lineofsight[1]] != None):
                    if (self.chess_array[lineofsight[0]][lineofsight[1]].get_color() != color):
                        pieceFound = True
                        temp.append(lineofsight)
                    break
                temp.append(lineofsight)
            if (not self.chess_array[x][y].get_capture_only_with_piece() or pieceFound):
                possible_moves2.extend(temp)

        # if (self.chess_array[x][y].get_name() == "q"):
        #     print("Now after debuffs ", possible_moves2)

        if (self.chess_array[x][y].get_is_debuffed()):
            possible_moves2 = self.chess_array[x][y].apply_debuff(
                possible_moves2)
        # print("After filtering, the possible moves for ", self.chess_array[x][y], " at ", x, "," , y, "" ,
        # " are ", possible_moves2)
        return possible_moves2

    def get_legal_moves(self, x, y):
        legal_moves = []
        color = self.chess_array[x][y].get_color()
        possible_moves = self.get_possible_moves(x, y, color)

        # Castling shit
        piece = self.chess_array[x][y]
        if piece.get_name() == "k":
            # white king
            if color == "white" and (x, y) == (7, 4):
                # King-side
                if self.chess_array[7][5] is None and self.chess_array[7][6] is None:
                    rook = self.chess_array[7][7]
                    if rook is not None and rook.get_name() == "r":
                        possible_moves.append((7, 6))  # K to g1

                # Queen-side
                if (self.chess_array[7][1] is None and
                    self.chess_array[7][2] is None and
                        self.chess_array[7][3] is None):
                    rook = self.chess_array[7][0]
                    if rook is not None and rook.get_name() == "r":
                        possible_moves.append((7, 2))

            # black king
            elif color == "black" and (x, y) == (0, 4):
                # King-side
                if self.chess_array[0][5] is None and self.chess_array[0][6] is None:
                    rook = self.chess_array[0][7]
                    if rook is not None and rook.get_name() == "r":
                        possible_moves.append((0, 6))

                # Queen-side
                if (self.chess_array[0][1] is None and
                    self.chess_array[0][2] is None and
                        self.chess_array[0][3] is None):
                    rook = self.chess_array[0][0]
                    if rook is not None and rook.get_name() == "r":
                        possible_moves.append((0, 2))

        newboard = self.clone_board_state()
        for move in possible_moves:
            if (newboard.moveprediction(move[0], move[1], x, y, color)):
                legal_moves.append(move)
        return legal_moves

    def returnLegalMoves(self, x, y):
        return self.chess_array[x][y].get_possible_moves()

    def update_all_legal(self):
        self.update_legal("white")
        self.update_legal("black")

    # Iterates and updates legal moves for a color
    def update_legal(self, color):
        countMoves = 0
        # Check if in check
        if (self.is_king_in_check(color)):
            print(color, "king in check")

        # Get specific piece list based on color
        pieceList = self.white_pieces.copy() if color == "white" else self.black_pieces.copy()

        # Go through piece list to get legal moves
        for x, y in pieceList:
            legal_moves = self.get_legal_moves(x, y)
            countMoves += len(legal_moves)
            self.chess_array[x][y].update_legal_moves(legal_moves)
        return countMoves

    def clone_board_state(self):
        # Set up a plane new board
        new_board = board(False)
        new_board.chess_array = [[None for j in range(8)] for i in range(8)]
        new_board.white_pieces = []
        new_board.black_pieces = []

        # Iterate through the old board and copy over
        for i in range(8):
            for j in range(8):
                piece = self.chess_array[i][j]
                if piece:
                    new_board.add_piece(i, j, piece.name, piece.color)
                    if (piece.color == "white"):
                        new_board.white_pieces.append((i, j))
                    if (piece.color == "black"):
                        new_board.black_pieces.append((i, j))
        return new_board

    def moveprediction(self, newx, newy, oldx, oldy, color):
        # Stores the deleted square if necessary
        temp = self.chess_array[newx][newy]
        # Are you landing on a square that's the same color as you? If so, return False
        if (temp != None and temp.get_color() == color):
            return False

        # checks if this move is valid; i.e. the king is not in check after this move
        validMove = False
        self.move_piece(newx, newy, oldx, oldy, color)
        if (not self.is_king_in_check(color)):
            validMove = True
        # Undoes any of the effects of the move
        self.move_piece(oldx, oldy, newx, newy, color)
        if (temp == None):
            return validMove

        # Resurrects the dead piece if the square we moved to wasn't none
        color = temp.get_color()
        if (color == "white"):
            self.white_pieces.append((newx, newy))
            self.chess_array[newx][newy] = temp
        if (color == "black"):
            self.black_pieces.append((newx, newy))
            self.chess_array[newx][newy] = temp
        return validMove

    def move_piece(self, newx, newy, oldx, oldy, color):
        if (color == "white"):
            self.white_pieces.remove((oldx, oldy))
            if ((newx, newy) in self.black_pieces):
                self.black_pieces.remove((newx, newy))
            self.white_pieces.append((newx, newy))
        else:
            self.black_pieces.remove((oldx, oldy))
            if ((newx, newy) in self.white_pieces):
                self.white_pieces.remove((newx, newy))
            self.black_pieces.append((newx, newy))
        self.chess_array[newx][newy] = self.chess_array[oldx][oldy]
        self.chess_array[newx][newy].update_coordinates(newx, newy)
        self.chess_array[newx][newy].firstMove = False
        self.chess_array[oldx][oldy] = None
        self.chess_array[newx][newy].find_moves(newx, newy)

        if (self.black_king_xy == (oldx, oldy)):
            self.black_king_xy = newx, newy
        if (self.white_king_xy == (oldx, oldy)):
            self.white_king_xy = newx, newy

        # brute-force rook movement
        moved_piece = self.chess_array[newx][newy]
        # King must be moving
        if moved_piece.get_name() == "k":
            # King-side castling
            if oldy == 4 and newy == 6:
                # White rook movement
                if color == "white" and oldx == 7:
                    rook = self.chess_array[7][7]
                    self.chess_array[7][7] = None
                    self.chess_array[7][5] = rook
                    self.white_pieces.remove((7, 7))
                    self.white_pieces.append((7, 5))
                    rook.find_moves(7, 5)

                # Black rook movement
                if color == "black" and oldx == 0:
                    rook = self.chess_array[0][7]
                    self.chess_array[0][7] = None
                    self.chess_array[0][5] = rook
                    self.black_pieces.remove((0, 7))
                    self.black_pieces.append((0, 5))
                    rook.find_moves(0, 5)

            # Queen-side castling
            if oldy == 4 and newy == 2:
                # White rook movement
                if color == "white" and oldx == 7:
                    rook = self.chess_array[7][0]
                    self.chess_array[7][0] = None
                    self.chess_array[7][3] = rook
                    self.white_pieces.remove((7, 0))
                    self.white_pieces.append((7, 3))
                    rook.find_moves(7, 3)

                # Black rook from movement
                if color == "black" and oldx == 0:
                    rook = self.chess_array[0][0]
                    self.chess_array[0][0] = None
                    self.chess_array[0][3] = rook
                    self.black_pieces.remove((0, 0))
                    self.black_pieces.append((0, 3))
                    rook.find_moves(0, 3)
