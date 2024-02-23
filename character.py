import pygame

#Create Character class
class Character:
    def __init__(self, width, height, x, y, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        
    