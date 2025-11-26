import pygame
from pygame.sprite import Sprite
import random


class PowerUp(Sprite):
    def __init__(self, ai_game, type_name):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.type = type_name

        if self.type == 'diamond':
            self.image = pygame.image.load('images/diamond.bmp')
        elif self.type == 'shield':
            self.image = pygame.image.load('images/shield.bmp')

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = self.screen_rect.bottom - self.rect.height

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Diamond(PowerUp):
    def __init__(self, ai_game):
        super().__init__(ai_game, 'diamond')


class Shield(PowerUp):
    def __init__(self, ai_game):
        super().__init__(ai_game, 'shield')