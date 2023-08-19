import pygame

# Import keys to control the game
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYUP,
    QUIT
)

pygame.init()

# Setting the Screen Width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Create the screen Object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


