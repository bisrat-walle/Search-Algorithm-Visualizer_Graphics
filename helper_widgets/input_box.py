import pygame as pg
from pygame.locals import *

# NOFRAME 

pg.init()
screen = pg.display.set_mode((400, 170), NOFRAME)
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
GRAY = (30, 30, 30)
FONT = pg.font.Font(None, 32)

green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 128)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(50, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

def drawText(text, x, y, color, fontSize=20):
    font = pg.font.Font('freesansbold.ttf', fontSize)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)


def main(alg="BFS"):
    clock = pg.time.Clock()
    input_box1 = InputBox(340, 50, 140, 30)
    input_boxes = [input_box1]
    button1 = pg.Rect(210, 100, 150, 40)
    button2 = pg.Rect(40, 100, 150, 40)
    done = False

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
                        print("Clicked 2")
            for box in input_boxes:
                box.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)
        pg.draw.rect(screen, green, button1)
        pg.draw.rect(screen, red, button2)
        drawText("CANCEL", 116, 120, blue)
        drawText("SEARCH", 280, 120, blue)
        drawText("Enter the number to be searched: ", 170, 65, green)
        drawText(f"Algorithm: {alg}", 170, 30, green, 22)

        pg.display.flip()
        clock.tick(30)
    
    pg.quit()


main()