import pygame

class Textbox():
    
    text = ""
    color = None
    box = None
    width = 0
    height = 0
    x = 0
    y = 0
    active = 0
    font = None
    default_text = ""

    def __init__(self, color, x, y, width, height, font_size, default_text = ""):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", font_size)
        self.color = color
        self.box = pygame.Rect(x,y,width,height)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.default_text = default_text

    def handle_textbox(self, screen, eventlist):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.box.collidepoint(pos):
                self.active = 1
                print("clicked textbox")
            else:
                self.active = 0

        for event in eventlist:
            if event.type == pygame.KEYDOWN and self.active == 1:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    temp_text = self.text
                    temp_text += event.unicode
                    if self.font.size(temp_text)[0] < self.width:
                        self.text += event.unicode
        if self.active == 0 and self.text == "" and self.default_text != "":
            pygame.draw.rect(screen, self.color, self.box)
            text_surface = self.font.render(self.default_text, False, (100,100,100))
            screen.blit(text_surface, (self.x, self.y))
            return
        pygame.draw.rect(screen, self.color, self.box)
        text_surface = self.font.render(self.text, False, (0,0,0))
        screen.blit(text_surface, (self.x, self.y))




