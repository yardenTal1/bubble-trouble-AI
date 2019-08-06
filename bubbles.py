import pygame
import copy

from settings import *


class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y, size, speed, image_name):
        pygame.sprite.Sprite.__init__(self)
        self.image_name = image_name
        self.image = pygame.image.load(IMAGES_PATH + image_name)
        self.image = pygame.transform.scale(self.image, (size*15, size*15))
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.size = size
        self.speed = speed

    def __eq__(self, other):
        if self.rect.centerx == other.rect.centerx and self.rect.centery == other.rect.centery:
            if self.size == other.size:
                return True
        return False

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > WINDOWWIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > WINDOWHEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.left = self._clip(self.rect.left, 0, WINDOWWIDTH)
        self.rect.right = self._clip(self.rect.right, 0, WINDOWWIDTH)
        self.rect.top = self._clip(self.rect.top, 0, WINDOWHEIGHT)
        self.rect.bottom = self._clip(self.rect.bottom, 0, WINDOWHEIGHT)

    @staticmethod
    def _clip(val, min_value, max_value):
        return min(max(val, min_value), max_value)


class Ball(Bubble):
    def __init__(self, x, y, size, speed):
        Bubble.__init__(self, x, y, size, speed, 'ball.png')

    def update(self):
        self.speed[1] += GRAVITY
        Bubble.update(self)

    def deep_copy_bubble(self):
        speed = copy.deepcopy(self.speed)
        return Ball(self.rect.centerx, self.rect.centerx, self.size, speed)


class Hexagon(Bubble):
    def __init__(self, x, y, size, speed):
        Bubble.__init__(self, x, y, size, speed, 'hexagon.png')

    def deep_copy_bubble(self):
        speed = copy.deepcopy(self.speed)
        return Hexagon(self.rect.centerx, self.rect.centerx, self.size, speed)
