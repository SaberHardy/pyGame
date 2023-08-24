import random
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surface = pygame.Surface((20, 20))
        self.surface.fill((255, 255, 255))
        self.rectangle = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = random.randint(5, 20)

    def update(self) -> None:
        self.rectangle.move_ip(-self.speed, 0)
        if self.rectangle.right < 0:
            self.kill()
