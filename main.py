import pygame
import os
import random
import character as ch
import enemies as en
import map

# Set Screen Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400

# Set up display
pygame.init()
pygame.display.set_caption("Quick Draw")
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
MAP = map.Map(SCREEN_WIDTH, SCREEN_HEIGHT, os.path.join("Assets", "background.jpg"))
BACKGROUND = pygame.transform.scale(pygame.image.load(MAP.background), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up player
PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "player_character.png"))
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

# Set up enemies
ENEMIES_IMAGE = pygame.image.load(os.path.join("Assets", "enemy_1.png"))
ENEMIES_WIDTH, ENEMIES_HEIGHT = 50, 50

#Set plain level
PLANE_LEVEL = 295

def draw_window(character, enemies):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(character.image, (character.rect.x, character.rect.y))
    for enemy in enemies:
        WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
    pygame.display.update()
    

def handle_enemies():
    enemies = []
    for i in range(5):
        enemies.append(en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), PLANE_LEVEL, ENEMIES_IMAGE))
    return enemies

# Handle player and enemy bullets
def handle_bullets():
    player_bullets = []
    enemy_bullets = []

def main():
    player_character = ch.Character(PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH//2, PLANE_LEVEL, PLAYER_IMAGE)
    #enemy_characters_init = en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), random.randint(100, 500), ENEMIES_IMAGE)
    enemy_characters = handle_enemies()
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        draw_window(player_character, enemy_characters)

if __name__ == "__main__":
    main()
