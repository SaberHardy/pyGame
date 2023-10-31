import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, isdir, join

pygame.init()

pygame.display.set_caption("2DGame")

BG_COLOR = (255, 255, 255)

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    X, Y, width, height = image.get_rect()

    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(widow, background, bg_image):
    for tile in background:
        widow.blit(bg_image, tile)

    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Purple.png")

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, bg_img)


if __name__ == "__main__":
    main(window)
