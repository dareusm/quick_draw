import pygame
import random

#Create Enemies class
class Enemies:
    def __init__(self, width, height, x, y, image, key):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.key = key
        key = []
    
    