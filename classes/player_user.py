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
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
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

        """Keep the object on the screen"""
        if self.rectangle.left < 0:
            self.rectangle.left = 0

        if self.rectangle.right > self.SCREEN_WIDTH:
            self.rectangle.right = self.SCREEN_WIDTH

        if self.rectangle.top <= 0:
            self.rectangle.top = 0

        if self.rectangle.bottom >= self.SCREEN_HEIGHT:
            self.rectangle.bottom = self.SCREEN_HEIGHT

