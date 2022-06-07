import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from collections import deque
from graphsearch.bfs import *
from graphsearch.dfs import *
from graphsearch.random_graph_generator import *

coordinateSize = (10, 6)
window_size = (1000, 600)
pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

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
        self.window = pygame.display.set_mode(window_size, DOUBLEBUF|OPENGL)
        gluOrtho2D(-1*coordinateSize[0], coordinateSize[0], -1*coordinateSize[1], coordinateSize[1])
        pygame.display.set_caption("Search Algorithm Visualizer")
        
        self.font = pygame.font.SysFont('arial', 35)
        self.startVisualizer()
    
    def draw_node(self, posX, posY, node):
        radius = .5
        angle = 2*np.pi/100
        glPolygonMode( GL_FRONT, GL_FILL )
        if not node.visited:
            glColor3f(1, 1, 1 )
        else:
            glColor3f(1, 1, 0)
        glBegin(GL_POLYGON)
        
        angle1 = 0.0
        glVertex2d(posX+radius * np.cos(0.0) , posY+radius * np.sin(0.0))
        for i in range(100):
            glVertex2d(posX+radius * np.cos(angle1), posY+radius * np.sin(angle1))
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


        """
        
            This function is responsible for drawing text on PyGame window
            
        """
        if not node.visited:
            textSurface = self.font.render(str(node.value), True, (0,255,0,255), (255,255,255,255))
        else:
            textSurface = self.font.render(str(node.value), True, (0,255,0,255), (255,255,0,255))
        text_data = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()
        glDrawPixels(textWidth, textHeight, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    def drawText(self, text, x, y, fontSize=25):
        textSurface = pygame.font.SysFont('arial', fontSize).render(text, True, (0,255,0,255), (255,255,255,255))
        text_data = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        textWidth = textSurface.get_width()
        textHeight = textSurface.get_height()
        glDrawPixels(textWidth, textHeight, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    def draw_edge_to_right_child(self, tempX, startY, helper, i):
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex2d(tempX+.5, startY)
        glVertex2d(tempX+helper[i+1][1]/2, startY-1)
        glEnd()
        glFlush()
    
    def draw_edge_to_left_child(self, tempX, startY, helper, i):
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex2d(tempX-.5, startY)
        glVertex2d(tempX-helper[i+1][1]/2, startY-1)
        glEnd()
        glFlush()
    
    
    def reset(self, graph):
        queue = deque([graph])
        while queue:
            current = queue.popleft()
            current.visited = False
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        
        
    def startVisualizer(self):
        graph = randomly_generate_graph()
        helper = {0:[0, 0], 1:[-4, 8], 2:[-6, 4], 3:[-7, 2]}
        search_generator = None
        iterations = 1
        finished = False
        input_box1 = InputBox(100, 100, 140, 32)
        input_boxes = [input_box1]
        while True:
            
            for event in pygame.event.get():
                for box in input_boxes:
                    box.handle_event(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_1 and not search_generator:
                        print("BFS")
                        search_generator = BFS(graph).search()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == K_2 and not search_generator:
                        print("DFS")
                        search_generator = DFS(graph).search()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == K_3 and search_generator and finished:
                        print("RESET")
                        self.reset(graph)
                        iterations = 1
                        search_generator = None
                        finished = False
                        
            if not finished and search_generator and iterations/5 == int(iterations/5):
                try:
                    search_generator.__next__()
                except StopIteration:
                    finished = True
                    pass
            
            
            keys = [
                "3 = RESET",
                "2 = DFS", 
                "1 = BFS",
            ]
            
            
            
            
            iterations += 1
            glClear(GL_COLOR_BUFFER_BIT)
            
            for index in range(len(keys)):
                self.drawText(keys[index], 10, 10+(index)*42)
            
            self.drawText("Search Algorithm Visualizer", 350, 30, 30)
            
            queue = deque([graph])
            i, startY = 0, 5
            while queue:
                tempX = helper[i][0]
                level_width = len(queue)
                for index in range(level_width):
                    current = queue.popleft()
                    self.draw_node(tempX, startY, current)
                    if current.left:
                        self.draw_edge_to_left_child(tempX, startY, helper, i)
                        queue.append(current.left)
                    if current.right:
                        self.draw_edge_to_right_child(tempX, startY, helper, i)
                        queue.append(current.right)
                    tempX += helper[i][1]
                    
                startY -= 1.5
                i += 1
            for box in input_boxes:
                pygame.Surface.blit(box, self.window, (0, 0))
            pygame.display.flip()
            pygame.time.wait(10)
            
            