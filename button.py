import pygame

class Button():

    name = ""
    callback = None
    sprite = None
    box = None

    def __init__(self, x, y, name, callback, filename, width, height, scale = 1):
        self.name = name
        self.callback = callback
        self.sprite = pygame.transform.scale(pygame.image.load(filename), (width*scale,height*scale))
        self.box = self.sprite.get_rect()
        self.box.topleft = (x,y)


    def draw(self,screen):
        self.handle_click()
        screen.blit(self.sprite,(self.box.x, self.box.y))

    def handle_click(self):
        pos = pygame.mouse.get_pos()

        if self.box.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                print(f"clicked {self.name}")
                self.callback
