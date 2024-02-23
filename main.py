import pygame
import os
import random
import character as ch
import enemies as en
import map

# Set Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Set up display
pygame.init()
pygame.display.set_caption("Quick Draw")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MAP = map.Map(SCREEN_WIDTH, SCREEN_HEIGHT, os.path.join("Assets", "background.jpg"))
BACKGROUND = pygame.transform.scale(pygame.image.load(MAP.background), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up player
PLAYER = pygame.image.load(os.path.join("Assets", "player.png"))
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

# Set up enemies
ENEMIES = pygame.image.load(os.path.join("Assets", "enemy.png"))
ENEMIES_WIDTH, ENEMIES_HEIGHT = 50, 50

player_character = ch.Character(PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH//2, 100, PLAYER)
enemy_characters = en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), random.randint(100, 500), ENEMIES)


def draw_window(character, enemies):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(character.image, (character.x, character.y))
    
    pygame.display.update()

def handle_enemies():
    enemies = []
    for i in range(5):
        enemies.append(enemy_characters)

# Handle player and enemy bullets
def handle_bullets():
    player_bullets = []
    enemy_bullets = []

def main():
    player_character = pygame.Rect(SCREEN_WIDTH//2, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        draw_window()

if __name__ == "__main__":
    main()
