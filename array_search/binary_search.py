from tkinter import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np
import time

root = Tk()
root.title('Binary Search Simulation')
root.geometry("700x700")


def init(self):

    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-10.0, 10.0, -4.0, 4.0)


def binary_search(nums, target, time):

    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right)//2
        if nums[mid] == target:
            return mid, True
        if nums[mid] < target:
            left = mid + 1
        else:
            left = mid - 1

    return mid
