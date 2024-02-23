import pygame

#Create Enemies class
class Enemies:
    def __init__(self, width, height, x, y, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
    
    