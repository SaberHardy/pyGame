import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, isdir, join

pygame.init()

pygame.display.set_caption("2DGame")

BG_COLOR = (255, 255, 255)

WIDTH, HEIGHT = 1000, 600
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_val = 0
        self.y_val = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_val = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_val = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    # This will call once every frame
    def loop(self, fps):
        self.y_val += min(1, (self.fall_count / fps) * self.GRAVITY)
        # moving the item
        self.move(self.x_val, self.y_val)
        self.fall_count += 1

    def draw(self, window):
        pygame.draw.rect(window, self.COLOR, self.rect)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    X, Y, width, height = image.get_rect()

    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(widow, background, bg_image, player):
    for tile in background:
        widow.blit(bg_image, tile)

    player.draw(window)
    pygame.display.update()


def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_val = 0

    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)


def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Purple.png")

    player = Player(100, 100, 50, 50)

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_img, player)


if __name__ == "__main__":
    main(window)
