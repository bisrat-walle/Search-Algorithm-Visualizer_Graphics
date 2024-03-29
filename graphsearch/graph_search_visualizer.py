import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from collections import deque
from graphsearch.bfs import *
from graphsearch.dfs import *
from graphsearch.random_graph_generator import *
from helper_widgets.input_box_tk import SearchInputReciever
import time

coordinateSize = (10, 6)
window_size = (1000, 600)


class GraphAlgorithmVisualizer:
    """

        This class is the main class of the project, which do the following:
            1. It instantiates pygame window
            2. It links the window created to PyOpenGL
            3. It finally visualizes Algorithms based on user input

    """

    def __init__(self):
        """


        """
        
        pygame.init()
        self.window = pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
        gluOrtho2D(-1*coordinateSize[0], coordinateSize[0], -
                   1*coordinateSize[1], coordinateSize[1])
        pygame.display.set_caption("Search Algorithm Visualizer")

        self.font = pygame.font.SysFont('arial', 35)
        self.res = False
        self.startVisualizer()
    
    def result(self):
        return self.res

    def draw_node(self, posX, posY, node):
        radius = .5
        angle = 2*np.pi/100
        
        gray = 128, 128, 128
        green = 0, 255, 0
        light_gray = 220/255, 220/255, 220/255
        
        glPolygonMode(GL_FRONT, GL_FILL)
        if node.target:
            glColor3f(0, 1, 0)
            self.found = True
        elif not node.visited:
            glColor3f(1, 1, 1)
        else:
            glColor3f(*light_gray)
        glBegin(GL_POLYGON)

        angle1 = 0.0
        glVertex2d(posX+radius * np.cos(0.0), posY+radius * np.sin(0.0))
        for i in range(100):
            glVertex2d(posX+radius * np.cos(angle1),
                       posY+radius * np.sin(angle1))
            angle1 += angle
        glEnd()
        glFlush()
        value = str(node.value)
        if len(value) == 1:
            self.drawNodeValue(node, window_size[0]/2+posX*window_size[0]/(coordinateSize[0]*2) - 10,
                               window_size[1]/2+posY*window_size[1]/(coordinateSize[1]*2)-18)
        else:
            self.drawNodeValue(node, window_size[0]/2+posX*window_size[0]/(coordinateSize[0]*2) - 16.7,
                               window_size[1]/2+posY*window_size[1]/(coordinateSize[1]*2)-21)

    def drawNodeValue(self, node, x, y):
        light_gray = 220, 220, 220
        """

            This function is responsible for drawing text on PyGame window

        """
        white = (255, 255, 255, 255)
        fg = (47, 79, 79, 255)

        if node.target:
            textSurface = self.font.render(
                str(node.value), True, fg, (0, 255, 0, 255))
        elif not node.visited:
            textSurface = self.font.render(
                str(node.value), True, fg, white)
        else:
            textSurface = self.font.render(
                str(node.value), True, fg, (*light_gray, 255))
        text_data = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()
        glDrawPixels(textWidth, textHeight, GL_RGBA,
                     GL_UNSIGNED_BYTE, text_data)

    def drawFooterBackground(self):
        glColor3f(0.1, .4, .5)
        glBegin(GL_QUADS)
        glVertex2d(-10, -3)
        glVertex2d(10, -3)
        glVertex2d(10, -6)
        glVertex2d(-10, -6)
        glEnd()
        glFlush()

    def drawText(self, text, x, y, fontSize=20, color=(255, 255, 255, 255), fgcolor=(0, 255, 0, 255)):
        textSurface = pygame.font.SysFont('monospace', fontSize).render(
            text, True, fgcolor, color)
        text_data = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()
        glDrawPixels(textWidth, textHeight, GL_RGBA,
                     GL_UNSIGNED_BYTE, text_data)

    def draw_edge_to_right_child(self, tempX, startY, helper, i, color=(0.9, .9, .9)):
        glLineWidth(3)
        glColor3fv(color)
        glBegin(GL_LINES)
        glVertex2d(tempX+.5, startY)
        glVertex2d(tempX+helper[i+1][1]/2, startY-1)
        glEnd()
        glFlush()

    def draw_edge_to_left_child(self, tempX, startY, helper, i, color=(0.9, .9, 0.9)):
        glLineWidth(3)
        glColor3fv(color)
        glBegin(GL_LINES)
        glVertex2d(tempX-.5, startY)
        glVertex2d(tempX-helper[i+1][1]/2, startY-1)
        glEnd()
        glFlush()

    def drawKeys(self, searching, alg="BFS", paused=False, completed=False, speed=1, target=-1, found=False):
        
        bg_color = 163, 214, 245
        self.drawText("BackSpace - to Return", 10, 550, 18, bg_color, (0, 0, 0))
        light_gray = 220/255, 220/255, 220/255
        
        if searching and not completed:
            self.drawText(f"Searching for: {target}", 420, 200, 18, bg_color, (0, 0, 0))
        
        if searching and completed:
            if found:
                self.drawText(f"{target} - Exists!", 430, 200, 18, bg_color, (0, 0, 0))
            else:
                self.drawText(f"{target} - Not Found!", 430, 200, 18, bg_color, (0, 0, 0))
        
        
        keys_top_right = [
            ["Unexplored", (3, 3.5), (1, 1, 1)],
            ["Visited", (3.84, 4.34), light_gray],
            ["Target", (4.68, 5.18), (0, 1, 0)],
        ]

        for index in range(len(keys_top_right)):
            self.drawText(keys_top_right[index][0],
                          820, 450+(index)*42, 18, bg_color, (0, 0, 0))

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
            "2 = DFS",
            "1 = BFS",
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
            self.drawText(keys_left[index], 10, 10 +
                          (index)*42, 18, (25.5, 102, 127.5))
        if searching:
            for index in range(len(keys_right)):
                self.drawText(keys_right[index], 750,
                              10+(index)*42, 18, (25.5, 102, 127.5))
        if completed:
            self.drawText("3 = RESET", 450, 94, 18, (25.5, 102, 127.5))

    def reset(self, graph):
        queue = deque([graph])
        while queue:
            current = queue.popleft()
            current.visited = False
            current.target = False
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        self.found = False

    def startVisualizer(self):
        graph = randomly_generate_graph()
        helper = {0: [0, 0], 1: [-4, 8], 2: [-6, 4], 3: [-7, 2]}
        search_generator = None
        finished = False
        paused = False
        last_time = None
        speed = 1
        running = True
        self.found = False
        
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1 and not search_generator:
                        input_ = SearchInputReciever("BFS")
                        target = input_.get_target()
                        if target != -1:
                            search_generator = BFS(graph).search(target)
                        last_time = time.time()
                    
                    if event.key == K_BACKSPACE:
                        self.res = True
                        running = False
                        

                    if event.key == K_2 and not search_generator:
                        input_ = SearchInputReciever("DFS")
                        target = input_.get_target()
                        if target != -1:
                            search_generator = DFS(graph).search(target)
                        last_time = time.time()

                    if event.key == K_3 and search_generator and finished:
                        print("RESET")
                        self.reset(graph)
                        search_generator = None
                        finished = False
                        self.Found = False
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
                    res = search_generator.__next__()
                    if res:
                        self.found = True
                        raise StopIteration()
                except StopIteration:
                    finished = True
                    speed = 1
                last_time = time.time()
            
            glClearColor(0.6367, 0.8359, 0.9570, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.drawFooterBackground()
            self.drawKeys(search_generator != None,
                          input_.alg if search_generator else "Unknown", paused, finished, speed, \
                          target if search_generator else -1, self.found)

            self.drawText("Search Algorithm Visualizer",
                          300, 30, 25, (25.5, 102, 127.5))
            self.drawText("© Developed by Bisrat and Yeabsira, 2022",
                          325, 10, 15, (25.5, 102, 127.5), (0, 0, 0))

            queue = deque([graph])
            i, startY = 0, 5
            while queue:
                tempX = helper[i][0]
                level_width = len(queue)
                for index in range(level_width):
                    current = queue.popleft()
                    self.draw_node(tempX, startY, current)
                    if current.left:
                        if current.left.visited:
                            self.draw_edge_to_left_child(
                                tempX, startY, helper, i, (0.1, .4, .5))
                        else:
                            self.draw_edge_to_left_child(
                                tempX, startY, helper, i)
                        queue.append(current.left)
                    if current.right:
                        if current.right.visited:
                            self.draw_edge_to_right_child(
                                tempX, startY, helper, i, (0.1, .4, .5))
                        else:
                            self.draw_edge_to_right_child(
                                tempX, startY, helper, i)
                        queue.append(current.right)
                    tempX += helper[i][1]

                startY -= 1.5
                i += 1

            pygame.display.flip()
            pygame.time.wait(10)
        
        pygame.quit()
