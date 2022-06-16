from cgitb import grey
from math import *
from tkinter import *
import pygame
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np
from array_search.node import *
from array_search.linear_search import *
from array_search.binary_search import *
from array_search.random_list_generator import *
from helper_widgets.input_box_tk import SearchInputReciever

coordinateSize = (10, 6)
window_size = (1000, 600)


def drawArray(array):
    """ Draws the given <array> """

    j = 0
    for i in range(-10, 10, 2):
        drawNode(i + 1, 0, array[j])
        j += 1


def drawNode(ox: int, oy: int, node: Node):
    """ Draws a circle with radius <r> from origin <ox, oy> """

    r = .65  # radius
    angle = 2*np.pi/100
    gray = 128, 128, 128
    green = 0, 255, 0

    def drawNodeValue(x: int, y: int, node: Node, fontSize: int = 25):
        """ Writes a text on the window """

        bg = None

        if node.isTarget:
            bg = (*green, 255)

        elif not node.visited:
            bg = (255, 255, 255, 255)
        elif node.visiting:
            bg = (1, 1, 1, 255)
        else:
            bg = (*gray, 255)

        textSurface = pygame.font.SysFont('arial', fontSize).render(
            str(node.val), True, (47, 79, 79, 255), bg)
        textData = pygame.image.tostring(textSurface, "RGBA", True)

        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, textData)

    glPolygonMode(GL_FRONT, GL_FILL)

    if node.isTarget:
        glColor3f(green[0]/256, green[1]/256, green[2]/256)
    elif node.visited:
        glColor3f(gray[0]/256, gray[1]/256, gray[2]/256)
    elif node.visiting:
        glColor3f(1, 0, 1)
    else:
        glColor3f(1, 1, 1)

    glBegin(GL_POLYGON)

    angle1 = 0.0
    glVertex2d(ox+r * np.cos(0.0), oy+r * np.sin(0.0))
    for i in range(100):
        glVertex2d(ox+r * np.cos(angle1),
                   oy+r * np.sin(angle1))
        angle1 += angle

    glEnd()
    glFlush()

    drawNodeValue(window_size[0]/2+ox*window_size[0]/(coordinateSize[0]*2) - 9,
                  window_size[1]/2+oy*window_size[1]/(coordinateSize[1]*2)-14, node)


def drawKeys(searching, alg="BFS", paused=False, completed=False, speed=1):

    keys_top_right = [
        ["Unexplored", (3, 3.5), (1, 1, 1)],
        ["Visited", (3.84, 4.34), (1, 1, 0)],
        ["Target", (4.68, 5.18), (0, 0, 1)],
    ]

    for index in range(len(keys_top_right)):
        drawText(keys_top_right[index][0],
                 820, 450+(index)*42, 18, (0, 0, 0))

    for index in range(len(keys_top_right)):
        glColor3fv(keys_top_right[index][2])
        glBegin(GL_QUADS)
        glVertex2d(9.0, keys_top_right[index][1][0])
        glVertex2d(9.5, keys_top_right[index][1][0])
        glVertex2d(9.5, keys_top_right[index][1][1])
        glVertex2d(9.0, keys_top_right[index][1][1])
        glEnd()
        glFlush()

    def getStatus():
        if completed:
            return "Completed"
        elif paused:
            return "Paused"
        return "Searching"

    keys_left = [
        "2 = Binary Search",
        "1 = Linear Search",
    ] if not searching else [
        f"Current Status: {getStatus()}",
        f"Current Speed : {speed}",
        f"Algorithm     : {alg}"
    ]

    keys_right = [
        "Space = Pause/Resume",
        "↓     = Speed down",
        "↑     = Speed up",
    ]

    for index in range(len(keys_left)):
        drawText(keys_left[index], 10, 10 +
                 (index)*42, 18, (25.5, 102, 127.5))
    if searching:
        for index in range(len(keys_right)):
            drawText(keys_right[index], 750,
                     10+(index)*42, 18, (25.5, 102, 127.5))
    if completed:
        drawText("3 = RESET", 450, 94, 18, (25.5, 102, 127.5))


def drawFooterBackground():

    glColor3f(0.1, .4, .5)
    glBegin(GL_QUADS)
    glVertex2d(-10, -3)
    glVertex2d(10, -3)
    glVertex2d(10, -6)
    glVertex2d(-10, -6)
    glEnd()
    glFlush()


def reset(array):

    for x in array:
        x.isTarget = False
        x.visited = False


def drawText(text, x, y, fontSize=20, color=(255, 255, 255, 255)):
    textSurface = pygame.font.SysFont('monospace', fontSize).render(
        text, True, (0, 255, 0, 255), color)
    text_data = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    textWidth = textSurface.get_width()
    textHeight = textSurface.get_height()
    glDrawPixels(textWidth, textHeight, GL_RGBA,
                 GL_UNSIGNED_BYTE, text_data)


def main():

    pygame.init()
    display = window_size
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glClearColor(0.6367, 0.8359, 0.9570, 1.0)

    xc, yc = coordinateSize
    gluOrtho2D(-xc, xc, -yc, yc)

    arr = random_list_generator()  # the array
    search_generator = None
    finished = False
    paused = False
    last_time = None
    speed = 1

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_1 and not search_generator:
                    input_ = SearchInputReciever("Linear Search")
                    target = input_.get_target()
                    if target != -1:
                        search_generator = linear_search(arr, target=target)
                    last_time = time.time()

                if event.key == K_2 and not search_generator:
                    input_ = SearchInputReciever("Binary Search")
                    target = input_.get_target()
                    if target != -1:
                        arr.sort(key=lambda x: x.val)
                        search_generator = binary_search(arr, target)
                    last_time = time.time()

                if event.key == K_3 and search_generator and finished:
                    reset(arr)
                    search_generator = None
                    finished = False
                    speed = 1

                if event.key == K_SPACE and search_generator and not finished:
                    paused = not paused
                    last_time = time.time()

                if event.key == K_UP and search_generator and not finished:
                    speed = min(4, speed+1)

                if event.key == K_DOWN and search_generator and not finished:
                    speed = max(1, speed-1)

        if not finished and not paused and search_generator and time.time() >= last_time+.5*(4-speed):
            try:
                search_generator.__next__()
            except StopIteration:
                finished = True
                speed = 1
            last_time = time.time()

        glClear(GL_COLOR_BUFFER_BIT)

        drawArray(arr)

        drawFooterBackground()
        drawKeys(search_generator != None,
                 input_.alg if search_generator else "Unknown", paused, finished, speed)

        drawText("Search Algorithm Visualizer",
                 300, 30, 25, (25.5, 102, 127.5))

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
