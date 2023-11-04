import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("2DGame")

BG_COLOR = (255, 255, 255)

WIDTH, HEIGHT = 1000, 600
FPS = 60
PLAYER_VEL = 6

window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    # load the image and split it
    images = [folder for folder in listdir(path) if isfile(join(path, folder))]
    # This will be key: animation style and value is: images in the animation
    all_sprites = {}
    # load all the different image files
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            # this will return to us load the images
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)  # blit = draw
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # the 98 in rect function is calculated from the top left of Terrain.png
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters",
                                 "MaskDude",
                                 32, 32,
                                 True)

    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.sprite = None
        self.rect = pygame.Rect(x, y, width, height)
        self.x_val = 0
        self.y_val = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def jump(self):
        self.y_val = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
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

        if self.hit:
            self.hit += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1

        self.update_sprite()

    def draw(self, window, offset_x):
        # pygame.draw.rect(window, self.COLOR, self.rect)

        # self.sprite = self.SPRITES['idle_' + self.direction][0]
        window.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    # update the rectangle that bounds the character based on the sprite that we're showing
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        # Do the mask: the masking is for mapping of all the pixels that exist in the Sprite
        # Any pixels perform on them perfect collision because we can overlap it with another mask
        self.mask = pygame.mask.from_surface(self.sprite)

    def landed(self):
        self.fall_count = 0
        self.y_val = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_val *= -1

    def update_sprite(self):
        sprite_sheet = 'idle'

        if self.hit:
            sprite_sheet = "hit"

        if self.y_val < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_val > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_val != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    X, Y, width, height = image.get_rect()

    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(widow, background, bg_image, player, objects, offset_x):
    for tile in background:
        widow.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()


def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_val = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collie = handle_vertical_collision(player, objects, player.y_val)
    to_check = [collide_left, collide_right, *vertical_collie]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        # fire.on()
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        # sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        # Do the mask: the masking is for mapping of all the pixels that exist in the Sprite
        # Any pixels perform on them perfect collision because we can overlap it with another mask
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)
    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_obj = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_obj = obj
            break
    # move it back
    player.move(-dx, 0)
    player.update()
    return collided_obj


def main(window):
    clock = pygame.time.Clock()
    background, bg_img = get_background("Purple.png")
    offset_x = 0
    scroll_area_width = 200

    block_size = 96
    player = Player(100, 100, 50, 50)

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    # blocks = [Block(0, HEIGHT - block_size, block_size)]

    fire.on()
    objects = [*floor,
               Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_img, player, objects, offset_x)

        #  checking if i'm moving to right
        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_val > 0) or \
                (player.rect.left - offset_x <= scroll_area_width and player.x_val < 0):
            offset_x += player.x_val

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
