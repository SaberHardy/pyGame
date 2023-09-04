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
        self.rect = self.surface.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        """Keep the object on the screen"""
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT

