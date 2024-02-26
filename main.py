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
BACKGROUND = pygame.transform.scale(
    pygame.image.load(MAP.background), (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Set up player
PLAYER_IMAGE = pygame.image.load(os.path.join("Assets", "player_character.png"))
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50

# Set up enemies
ENEMIES_IMAGE = pygame.image.load(os.path.join("Assets", "enemy_1.png"))
ENEMIES_WIDTH, ENEMIES_HEIGHT = 50, 50

# Set plain level
PLANE_LEVEL = 295

# Create User Events
ENEMYSPAWN = pygame.USEREVENT + 1
ENEMYHIT = pygame.USEREVENT + 2
PLAYERHIT = pygame.USEREVENT + 3

# Set bullet speed
BULLET_VEL = 10


def enemy_spawn_timer():
    timer = pygame.time.set_timer(
        ENEMYSPAWN, 3000
    )  # Trigger enemy spawn every 3 seconds
    return timer


def draw_window(character, enemies, player_bullets, enemy_bullets):
    # Draw Background
    WIN.blit(BACKGROUND, (0, 0))

    # Draw Character
    WIN.blit(character.image, (character.rect.x, character.rect.y))

    font = pygame.font.SysFont("Comicsans", 30)

    # Draw enemies
    for enemy in enemies:
        # Keeping all enemies on the screen
        if enemy.rect.x < 0:
            enemy.rect.x = 0
        elif enemy.rect.x > SCREEN_WIDTH:
            enemy.rect.x = SCREEN_WIDTH - enemy.rect.width

        # Flip the enemy image if the enemy is facing the opposite direction
        if enemy.rect.x > character.rect.x and enemy.facing_right:
            enemy.image = pygame.transform.flip(enemy.image, True, False)
            enemy.facing_right = False
        elif enemy.rect.x < character.rect.x and not enemy.facing_right:
            enemy.image = pygame.transform.flip(enemy.image, True, False)
            enemy.facing_right = True

        # Check if the enemy is on the same x coordinate as the character
        if (
            enemy.rect.x == character.rect.x
            or enemy.rect.x == character.rect.x + 20
            or enemy.rect.x == character.rect.x - 20
        ):
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.x)

        WIN.blit(enemy.image, (enemy.rect.x, enemy.rect.y))

        # Render the key to a surface
        key_surface = font.render(enemy.key, 1, (255, 255, 255))

        # Draw the key above the enemy
        WIN.blit(
            key_surface, (enemy.rect.x + 15, enemy.rect.y - key_surface.get_height())
        )

        # Draw player bullets
    for bullet in player_bullets:
        pygame.draw.rect(WIN, (255, 0, 0), bullet)

    # Draw enemy bullets
    for bullet in enemy_bullets:
        pygame.draw.rect(WIN, (0, 0, 255), bullet)

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
            enemies.append(
                en.Enemies(
                    ENEMIES_WIDTH,
                    ENEMIES_HEIGHT,
                    random.randint(100, 700),
                    PLANE_LEVEL,
                    ENEMIES_IMAGE,
                    key,
                )
            )
            enemies = assign_random_key_to_enemies(enemies)
    return enemies


# Handle player and enemy bullets
"""
def handle_bullets(player_bullets, enemy_bullets, player, enemies):
    for player_bullet in player_bullets:
        if enemies.x > player.x:
            player_bullet.x += BULLET_VEL
            if enemies.colliderect(player_bullet):
                pygame.event.post(ENEMYHIT)
                player_bullets.remove(player_bullet)
        if enemies.x < player.x:
            player_bullet.x -= BULLET_VEL
            if enemies.colliderect(player_bullet):
                pygame.event.post(ENEMYHIT)
                player_bullets.remove(player_bullet)

    for enemy_bullet in enemy_bullets:
        if player.x > enemies.x:
            enemy_bullet.x += BULLET_VEL
            if player.colliderect(enemy_bullet):
                pygame.event.post(PLAYERHIT)
                enemy_bullets.remove(enemy_bullet)
            if player.x < enemies.x:
                enemy_bullet.x -= BULLET_VEL
                if player.colliderect(enemy_bullet):
                    pygame.event.post(PLAYERHIT)
                    enemy_bullets.remove(enemy_bullet)
"""

def handle_bullets(player_bullets, enemy_bullets, player, enemies):
    for player_bullet in player_bullets:
        for enemy in enemies:
            if enemy.rect.x > player.rect.x:
                player_bullet.x += BULLET_VEL
                if enemy.rect.colliderect(player_bullet):
                    pygame.event.post(pygame.event.Event(ENEMYHIT))
                    player_bullets.remove(player_bullet)
            elif enemy.rect.x < player.rect.x:
                player_bullet.x -= BULLET_VEL
                if enemy.rect.colliderect(player_bullet):
                    pygame.event.post(pygame.event.Event(ENEMYHIT))
                    player_bullets.remove(player_bullet)

    for enemy_bullet in enemy_bullets:
        if player.rect.x > enemy.rect.x:
            enemy_bullet.x += BULLET_VEL
            if player.rect.colliderect(enemy_bullet):
                pygame.event.post(pygame.event.Event(PLAYERHIT))
                enemy_bullets.remove(enemy_bullet)
        elif player.rect.x < enemy.rect.x:
            enemy_bullet.x -= BULLET_VEL
            if player.rect.colliderect(enemy_bullet):
                pygame.event.post(pygame.event.Event(PLAYERHIT))
                enemy_bullets.remove(enemy_bullet)


def main():
    player_character = ch.Character(
        PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH // 2, PLANE_LEVEL, PLAYER_IMAGE
    )
    # enemy_characters_init = en.Enemies(ENEMIES_WIDTH, ENEMIES_HEIGHT, random.randint(100, 700), random.randint(100, 500), ENEMIES_IMAGE)
    enemy_characters = []

    # Bullets
    player_bullets = []
    enemy_bullets = []

    clock = pygame.time.Clock()
    last_shot_time = pygame.time.get_ticks()  # Initialize last_shot_time
    run = True
    enemy_spawn_timer()
    while run:
        current_time = pygame.time.get_ticks()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == ENEMYSPAWN:
                key = get_random_key()
                enemy_characters.append(
                    en.Enemies(
                        ENEMIES_WIDTH,
                        ENEMIES_HEIGHT,
                        random.randint(100, 700),
                        PLANE_LEVEL,
                        ENEMIES_IMAGE,
                        get_random_key(),
                    )
                )
                enemy_characters = assign_random_key_to_enemies(enemy_characters)

            if event.type == pygame.KEYDOWN:
                for enemy in enemy_characters:
                    if event.unicode == enemy.key:
                        if current_time - last_shot_time > 1000:  # Fire rate control (1 shot per second)
                            """
                            bullet = pygame.Rect(player_character.rect.x + player_character.rect.width, player_character.rect.y + player_character.rect.height // 2, 10, 5)
                            player_bullets.append(bullet)
                            last_shot_time = current_time
                            """
                            if enemy.rect.x > player_character.rect.x:
                                bullet = pygame.Rect(player_character.rect.x + player_character.rect.width, SCREEN_WIDTH - PLANE_LEVEL - (player_character.rect.height // 3), 10, 5)
                                player_bullets.append(bullet)
                                last_shot_time = current_time
                            if enemy.rect.x < player_character.rect.x:
                                bullet = pygame.Rect(player_character.rect.x, SCREEN_WIDTH - PLANE_LEVEL - (player_character.rect.height // 3), 10, 5)
                                player_bullets.append(bullet)
                                last_shot_time = current_time
                                

        handle_bullets(player_bullets, enemy_bullets, player_character, enemy_characters)
        draw_window(player_character, enemy_characters, player_bullets, enemy_bullets)


if __name__ == "__main__":
    main()
