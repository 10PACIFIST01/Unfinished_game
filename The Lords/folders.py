import os
import pygame

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
friedrich_folder = os.path.join(img_folder, "friedrich")
env_folder = os.path.join(img_folder, "environment")
map_folder = os.path.join(game_folder, "locations")
map_name = os.path.join(map_folder, "field.txt")
front_friedrich_folder = os.path.join(friedrich_folder, "front")


def load(folder, file_name, exp, num=0):
    if num:
        images = []
        for i in range(num):
            name = os.path.join(folder, file_name + str(i) + exp)
            image = pygame.image.load(name)
            images += [image]
        return images
    else:
        name = os.path.join(folder, file_name + exp)
        image = pygame.image.load(name)
        return image


def image_name(folder, name):
    return os.path.join(folder, name)
