import pygame as pg
from pygame.locals import *

GRAY = (30, 30, 30)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 128)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.COLOR_INACTIVE = pg.Color('lightskyblue3')
        self.COLOR_ACTIVE = pg.Color('dodgerblue2')
        self.FONT = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        width = max(50, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

class SearchInputReciever:
    def __init__(self, alg):
        self.alg = alg
        self.result = None
        self.screen = pg.display.set_mode((400, 170), NOFRAME)

    def drawText(self, text, x, y, color, fontSize=20):
        font = pg.font.Font('freesansbold.ttf', fontSize)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)


    def receiveInput(self):
        clock = pg.time.Clock()
        input_box1 = InputBox(340, 50, 140, 30)
        input_boxes = [input_box1]
        button1 = pg.Rect(210, 100, 150, 40)
        button2 = pg.Rect(40, 100, 150, 40)
        done = False
        cancel = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if button1.collidepoint(event.pos):
                            done=True
                            print("Clicked 1")
                        if button2.collidepoint(event.pos):
                            done=True
                            cancel = True
                            print("Clicked 2")
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(self.screen)
            pg.draw.rect(self.screen, green, button1)
            pg.draw.rect(self.screen, red, button2)
            self.drawText("CANCEL", 116, 120, blue)
            self.drawText("SEARCH", 280, 120, blue)
            self.drawText("Enter the number to be searched: ", 170, 65, green)
            self.drawText(f"Algorithm: {self.alg}", 170, 30, green, 22)

            pg.display.flip()
            clock.tick(30)
        
        pg.quit()
        self.result = (not cancel, input_box1.text)

if __name__ == "__main__":      
    pg.init()
    input_ = SearchInputReciever("BFS")
    input_.receiveInput()
