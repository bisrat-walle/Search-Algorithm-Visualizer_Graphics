from math import *
from tkinter import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np
from node import *
from random_list_generator import *

coordinateSize = (13, 13)
window_size = (800, 800)


def drawText(x: int, y: int, node: Node, fontSize: int = 25):
    """ Writes a text on the window """

    bg = None
    if node.isTarget:
        bg = (0, 0, 255, 255)
    elif not node.visited:
        bg = (255, 255, 255, 255)
    else:
        bg = (255, 255, 0, 255)

    textSurface = pygame.font.SysFont('arial', fontSize).render(
        str(node.val), True, (0, 255, 0, 255), bg)
    textData = pygame.image.tostring(textSurface, "RGBA", True)

    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def drawArray(arr):

    j = 0
    for i in range(-12, 12, 3):
        drawCircle(i + 1.5, 0, arr[j])
        j += 1


def drawCircle(ox: int, oy: int, node: Node):
    """ Draws a circle with radius <r> from origin <ox, oy> """

    r = 1  # radius

    glPolygonMode(GL_FRONT, GL_FILL)

    if node.isTarget:
        glColor3f(0, 0, 1)
    elif not node.visited:
        glColor3f(1, 1, 1)
    else:
        glColor3f(1, 1, 0)

    glBegin(GL_POLYGON)

    for i in range(1000):
        angle = 2 * pi * i / 1000

        x = r * cos(angle) + ox
        y = r * sin(angle) + oy

        glVertex2f(x, y)

    glEnd()
    glFlush()

    drawText(window_size[0]/2+ox*window_size[0]/(coordinateSize[0]*2) - 9,
             window_size[1]/2+oy*window_size[1]/(coordinateSize[1]*2)-14, node)


def main():

    pygame.init()
    display = window_size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.6367, 0.8359, 0.9570, 1.0)

    xc, yc = coordinateSize
    gluOrtho2D(-xc, xc, -yc, yc)

    arr = random_list_generator()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT)

        drawArray(arr)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
