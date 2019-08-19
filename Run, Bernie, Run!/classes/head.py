from random import randint
import pygame

class Head():
    def __init__(self, settings, top, screen, speed_factor, right=660):
        self.settings = settings
        self.speed_factor = speed_factor
        self.path = 'images/heads/head' + str(randint(1, settings.number_of_heads)) + '.bmp'
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()
        self.rect.right = right
        self.rect.top = top
        self.screen = screen
        self.is_off_screen = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.right -= self.settings.speed_of_heads_x * self.speed_factor
        if self.rect.right <= 0:
            self.is_off_screen = True
