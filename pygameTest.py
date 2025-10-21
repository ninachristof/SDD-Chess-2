import pygame
import sys

# --- CONFIG ---
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
SELECTED = (246, 246, 105)

# Simple 2D array for board state
# Each piece represented as a single char: uppercase = white, lowercase = black
# (R = Rook, N = Knight, B = Bishop, Q = Queen, K = King, P = Pawn)
board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minimal Chess UI")
font = pygame.font.SysFont("Arial", 44)

selected_square = None
running = True

# --- FUNCTIONS ---
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            if selected_square == (row, col):
                color = SELECTED
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != " ":
                text = font.render(piece, True, (0,0,0))
                text_rect = text.get_rect(center=(col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2))
                win.blit(text, text_rect)

def get_square_under_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def move_piece(start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    board[sr][sc] = " "
    board[er][ec] = piece

# --- GAME LOOP ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            row, col = get_square_under_mouse(pos)
            if selected_square:
                move_piece(selected_square, (row, col))
                selected_square = None
            else:
                if board[row][col] != " ":
                    selected_square = (row, col)

    draw_board(screen)
    draw_pieces(screen)
    pygame.display.flip()
