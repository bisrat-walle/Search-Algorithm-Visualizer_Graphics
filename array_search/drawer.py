from math import *
from tkinter import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np


def drawText(x: int, y: int, text: int or str, color: tuple, fontSize: int = 25):

    textSurface = pygame.font.SysFont('arial', fontSize).render(
        str(text), True, (0, 255, 0, 255), (1, 1, 1, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)

    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def drawCircle(ox: int, oy: int, r: int, num: int, color: tuple = (1, 0, 0)):
    """ Draws a circle with radius <r> from origin <ox, oy> """

    drawText(3, 0, 1000, (10, 0, 10))

    glPolygonMode(GL_BACK, GL_FILL)
    glColor3f(*color)

    glBegin(GL_POLYGON)

    for i in range(1000):
        angle = 2 * pi * i / 1000

        x = r * cos(angle) + ox
        y = r * sin(angle) + oy

        glVertex2f(x, y)

    print('x is ', x, 'y is ', y)


def main():

    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        drawCircle(0, 0, 3, 10)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
