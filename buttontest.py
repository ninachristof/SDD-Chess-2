import pygame
import sys
from button import *
from colors import *

def callback_1():
    print("callback 1")

def callback_2():
    print("callback 2")

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))


button_width = 300
button_height = 100
xpos = (WIDTH - button_width) //2
ypos = (HEIGHT - button_height) //2
#button = TextButton(color,x,y,width, height, font_size, text, callback):
text_0 = "button and no callback"
text_1 = "button with callback and text overflow"
text_2 = "button with callback"
button_0 = TextButton(c.LIGHT_BLUE_1,xpos,ypos-300,button_width, button_height, button_height//2 - 10, text_0, None)
button_1 = TextButton(c.WHITE,xpos,ypos,button_width, button_height, button_height//2 - 10, text_1, callback_1)
button_2 = TextButton(c.LIGHT_BLUE_2,xpos,ypos + 300,button_width, button_height, button_height//2 - 10, text_2, callback_2)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(c.BOARD_GREEN)
    button_0.draw(screen)
    button_1.draw(screen)
    button_2.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()

