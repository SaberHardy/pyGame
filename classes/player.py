import pygame
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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((75, 25))
        self.surface.fill((255, 255, 255))
        print('user printed')
        self.rectangle = self.surface.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rectangle.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rectangle.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rectangle.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rectangle.move_ip(5, 0)
