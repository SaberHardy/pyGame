import pygame
from classes.player import Player

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

# This object is created from the player class that inherits from Player Main class
player = Player()
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((player.SCREEN_WIDTH, player.SCREEN_HEIGHT))

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # This will return a set of keys and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Turn the screen from black(Default color) to White color
    # screen.fill((255, 255, 255))
    #
    # surface = pygame.Surface((100, 100))
    #
    # Fill the small rectangle with black color
    screen.fill((0, 0, 0))
    # rectangle = surface.get_rect()

    # surface_center = (
    #     (SCREEN_WIDTH - surface.get_width()) / 2,
    #     (SCREEN_HEIGHT - surface.get_height()) / 2)

    # This line will display the rectangle from Top left corner
    screen.blit(player.surface, player.rectangle)

    # This will display the rectangle in the center of the screen
    # screen.blit(player.surface, surface_center)

    pygame.display.flip()

# User Input
