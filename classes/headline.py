from random import randint
import pygame

class Headline():
    def __init__(self, top, screen, settings):
        self.path = 'images/headlines/600x100/headline' + str(randint(1, settings.number_of_headlines)) + '.bmp'
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = top
        self.screen = screen
        self.settings = settings
        self.is_off_screen = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.rect.top -= self.settings.headline_scroll_speed
        if self.rect.bottom <= 0:
            self.is_off_screen = True
