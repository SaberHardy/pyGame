import pygame

from classes.enemy import Enemy
from classes.player_user import Player

# Import keys to control the game
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYUP,
    KEYDOWN,
    QUIT
)

pygame.init()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# This object is created from the player class that inherits from Player Main class
player = Player()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((player.SCREEN_WIDTH, player.SCREEN_HEIGHT))

enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # This will return a set of keys and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    # Turn the screen from black(Default color) to White color
    # screen.fill((255, 255, 255))
    #
    # surface = pygame.Surface((100, 100))
    #
    # Fill the small rect with black color
    screen.fill((0, 0, 0))
    # rect = surface.get_rect()

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surface, entity.rect)
    # surface_center = (
    #     (SCREEN_WIDTH - surface.get_width()) / 2,
    #     (SCREEN_HEIGHT - surface.get_height()) / 2)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # This line will display the rect from Top left corner
    screen.blit(player.surface, player.rect)

    # This will display the rect in the center of the screen
    # screen.blit(player.surface, surface_center)

    pygame.display.flip()

# Collision Detection
