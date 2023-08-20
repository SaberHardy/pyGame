import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = pygame.Surface((75, 25))
        self.surface.fill((255, 255, 255))
        print('user printed')
        self.rectangle = self.surface.get_rect()
