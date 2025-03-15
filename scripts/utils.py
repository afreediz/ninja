import pygame
import os

BASE_DIR = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_DIR + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img in sorted(os.listdir(BASE_DIR + path)):
        images.append(load_image(path + img))

    return images