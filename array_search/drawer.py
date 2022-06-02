from math import *
from tkinter import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np


def init():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)


def drawText(x, y, text, fontSize=25):

    glClear(GL_COLOR_BUFFER_BIT)

    font = pygame.font.SysFont('arial', fontSize)

    textSurface = font.render(
        str(text), True, (0, 255, 0, 255), (255, 255, 255, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)

    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def drawCircle(ox: int, oy: int, r: int, segment: int, num: int, color: tuple = (240, 1, 1)):
    """ Draws a circle with radius <r> from origin <ox, oy> """

    drawText(ox, oy, "1008")

    glPolygonMode(GL_BACK, GL_FILL)
    glColor3f(*color)

    glBegin(GL_POLYGON)

    for i in range(segment):
        angle = 2 * pi * i / segment

        x = r * cos(angle) + ox
        y = r * sin(angle) + oy

        glVertex2f(x, y)

    glEnd()
    glFlush()


def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        drawCircle(0, 0, 3, 10**3, 10)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
