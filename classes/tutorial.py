import pygame

class Tutorial():
    def __init__(self, screen, settings):
        # keep track of screen
        self.screen = screen

        # keep track of settings
        self.settings = settings

        # load tutorial
        self.slides = []
        for num in range(1, 17):
            self.slides.append(pygame.image.load('images/tutorial/tutorial' + str(num) + '.bmp'))

        # rect for slides
        self.rect = self.slides[0].get_rect()
        self.rect.top = 0
        self.rect.left = 0

        # keep track of current slide
        self.curr_slide = 0

    def draw(self):
        self.screen.blit(self.slides[self.curr_slide], self.rect)
        pygame.display.update()

    def update(self):
        if self.curr_slide < 15:
            self.curr_slide += 1
        else:
            self.curr_slide = 0
            self.settings.mode = 'title'
            self.settings.selector = 'play'
