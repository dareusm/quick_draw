import pygame
import os
import random
import character as ch
import enemies as en
import map
import string
pygame.font.init()

# Set up alphabet variable
alphabet = list(string.ascii_lowercase)

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

# Set plain level
PLANE_LEVEL = 295

# Create User Event
ENEMYSPAWN = pygame.USEREVENT + 1

def enemy_spawn_timer():
    timer = pygame.time.set_timer(
        ENEMYSPAWN, 3000
    )  # Trigger enemy spawn every 3 seconds
    return timer

def draw_window(character, enemies):
    # Draw Background
    WIN.blit(BACKGROUND, (0, 0))

    # Draw Character
    WIN.blit(character.image, (character.rect.x, character.rect.y))

    font = pygame.font.SysFont("Comicsans", 30)

    # Draw enemies
    for enemy in enemies:
        #Keeping all enemies on the screen
        if enemy.rect.x < 0:
            enemy.rect.x = 0
        elif enemy.rect.x > SCREEN_WIDTH:
            enemy.rect.x = SCREEN_WIDTH - enemy.rect.width

        #Flip the enemy image if the enemy is facing the opposite direction
        if enemy.rect.x > character.rect.x and enemy.facing_right:
            enemy.image = pygame.transform.flip(enemy.image, True, False)
            enemy.facing_right = False
        elif enemy.rect.x < character.rect.x and not enemy.facing_right:
            enemy.image = pygame.transform.flip(enemy.image, True, False)
            enemy.facing_right = True
        
        #Check if the enemy is on the same x coordinate as the character
        if enemy.rect.x == character.rect.x or enemy.rect.x == character.rect.x + 20 or enemy.rect.x == character.rect.x - 20:
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.x)

        WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

        # Render the key to a surface
        key_surface = font.render(enemy.key, 1, (255, 255, 255))

        # Draw the key above the enemy
        WIN.blit(key_surface, (enemy.rect.x+15, enemy.rect.y - key_surface.get_height()))

    # Update Display
    pygame.display.update()

# Get random key from alphabet list
def get_random_key():
    return random.choice(alphabet)

# Assign a random key to enemies
def assign_random_key_to_enemies(enemies):
    for enemy in enemies:
        enemy.key = get_random_key()
    return enemies

def handle_enemies():
    enemies = []
    key = ""
    for i in range(5):
        for event in pygame.event.get():
            enemies.append(en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), PLANE_LEVEL, ENEMIES_IMAGE, key))
            enemies = assign_random_key_to_enemies(enemies)
    return enemies 

# Handle player and enemy bullets
def handle_bullets():
    player_bullets = []
    enemy_bullets = []

def main():
    player_character = ch.Character(PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH//2, PLANE_LEVEL, PLAYER_IMAGE)
    #enemy_characters_init = en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), random.randint(100, 500), ENEMIES_IMAGE)
    enemy_characters = []
    
    clock = pygame.time.Clock()
    run = True
    enemy_spawn_timer()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == ENEMYSPAWN:
                key = get_random_key()
                enemy_characters.append(en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), PLANE_LEVEL, ENEMIES_IMAGE, get_random_key()))
                enemy_characters = assign_random_key_to_enemies(enemy_characters)
        draw_window(player_character, enemy_characters)

if __name__ == "__main__":
    main()
