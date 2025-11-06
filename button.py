import pygame

#TODO: inheritence here

class Button():

    text = ""
    color = None
    box = None
    width = 0
    height = 0
    x = 0
    y = 0
    font = None
    callback = None

    def __init__(self,color,x,y,width, height, font_size, text, callback):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", font_size)
        self.color = color
        self.box = pygame.Rect(x,y,width,height)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.callback = callback

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.box)
        text_surface = self.font.render(self.text, False, (0,0,0))
        screen.blit(text_surface, (self.x, self.y))
        return self.handle_click()


    def handle_click(self):
        pos = pygame.mouse.get_pos()

        if self.box.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.callback != None:
                    print("hi")
                    self.callback
                return 1 
        return 0

class ImageButton():

    callback = None
    sprite = None
    box = None

    def __init__(self, x, y, callback, filename, width, height, scale = 1):
        self.callback = callback
        self.sprite = pygame.transform.scale(pygame.image.load(filename), (width*scale,height*scale))
        self.box = self.sprite.get_rect()
        self.box.topleft = (x,y)


    def draw(self,screen):
        screen.blit(self.sprite,(self.box.x, self.box.y))
        return self.handle_click()

    def handle_click(self):
        pos = pygame.mouse.get_pos()

        if self.box.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.callback
                return 1 
        return 0
