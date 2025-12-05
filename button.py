import pygame

class Button():

    box = None
    width = 0
    height = 0
    x = 0
    y = 0
    callback = None
    args = None
    kwargs = None

    def __init__(self,x,y,width, height, callback, *args, **kwargs):
        self.box = pygame.Rect(x,y,width,height)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        if self.box.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                if self.callback != None:
                    #print("CALLBACK:",self.callback)
                    self.callback(*self.args, **self.kwargs)
                return 1 
        return 0

class TextButton(Button):

    font = None
    text = ""
    color = None

    def __init__(self,color,x,y,width, height, font_size, text, callback, *args, **kwargs):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", font_size)
        #self.font = pygame.font.Font("resources/Coolvetica Rg.otf", font_size)
        self.color = color
        self.box = pygame.Rect(x,y,width,height)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.hover = True

    def draw(self,screen):
        pos = pygame.mouse.get_pos()
        outline = pygame.Rect(self.x-1,self.y-1,self.width+1,self.height+1)
        if not self.box.collidepoint(pos) or not self.hover:
            pygame.draw.rect(screen, self.color, self.box,width = 0, border_radius = 2)
        else:
            darker_color = (max(self.color[0]-20,0),max(self.color[1]-20,0),max(self.color[2]-20,0))
            pygame.draw.rect(screen,darker_color, self.box,width = 0, border_radius = 2)

        pygame.draw.rect(screen, "black",outline,2,3)
        text_words = self.text.split()
        text_lines = []
        curr_line = ""
        for word in text_words:

            #if curr_line == "" :
            #    curr_line += word
            if self.font.size(curr_line + " " + word)[0] <= self.width:
                curr_line += " " + word
            else:
                text_lines.append(curr_line)
                curr_line = " " + word
        if curr_line != "":
            text_lines.append(curr_line)
        text_surface = []

        for i in range(len(text_lines)):
            text_surface = (self.font.render(text_lines[i], False, (0,0,0)))
            screen.blit(text_surface, (self.x, self.y + (i * self.font.get_height())))
        return self.handle_click()

class ImageButton(Button):

    callback = None
    sprite = None
    filename = ""
    

    def __init__(self, x, y, width, height, filename, scale, callback, *args, **kwargs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filename = filename
        self.callback = callback
        self.sprite = pygame.transform.scale(pygame.image.load(filename), (width*scale,height*scale))
        self.box = self.sprite.get_rect()
        self.box.topleft = (x,y)
        self.args = args
        self.kwargs = kwargs

    def draw(self,screen):
        screen.blit(self.sprite,(self.box.x, self.box.y))
        return self.handle_click()
