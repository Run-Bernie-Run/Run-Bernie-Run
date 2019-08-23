import pygame


class Bernie():
    def __init__(self, settings):
        # initialize width and height data members
        self.width = settings.bernie_width
        self.height = settings.bernie_height

        # give bernie object access to settings object
        self.settings = settings

        # create list of frames
        self.frames = []
        self.frames.append(pygame.image.load('images/bernie_running_animation/0.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/1.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/2.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/3.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/4.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/5.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/6.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/7.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/8.bmp'))
        self.frames.append(pygame.image.load('images/bernie_running_animation/9.bmp'))

        # keep track of current frame number
        self.current_frame_number = 0

        # initialize initial frame
        self.current_frame = self.frames[0]

        # bernie starts off not jumping
        self.is_jumping = False

        # initialize rect data member
        self.rect = self.current_frame.get_rect()
        self.rect.bottom = settings.bernie_start_bottom
        self.rect.left = settings.bernie_left

        # initialize boolean vars
        self.is_jumping = False
        self.is_falling = False
        self.is_on_ground = True

        # create bernie's hit box
        self.hit_box = pygame.Rect(0, 0, 80, 80)
        self.hit_box.centerx = self.rect.centerx
        self.hit_box.centery = self.rect.centery

        # for invicibility frames
        self.is_invincible = False
        self.invincible_until = -1


    def update_animation_cycle(self):
        # cycle through frames
        if self.current_frame_number <= 8:
            self.current_frame_number += 1
            self.current_frame = self.frames[self.current_frame_number]
        else:
            self.current_frame_number = 0
            self.current_frame = self.frames[self.current_frame_number]

    def update_jumping(self):
        # go up if jumping
        if self.is_jumping:
            self.rect.bottom -= self.settings.bernie_jump_update
            # start falling if we reach maximum height
            if self.rect.top <= self.settings.bernie_max_height_of_top:
                self.is_jumping = False
                self.is_falling = True
        # go down is falling
        elif self.is_falling:
            self.rect.bottom += self.settings.bernie_jump_update
            # stop falling if we reach the ground
            if self.rect.bottom == self.settings.bernie_start_bottom:
                self.is_falling = False
                self.is_on_ground = True
            elif self.rect.bottom > self.settings.bernie_start_bottom:
                self.rect.bottom = self.settings.bernie_start_bottom
                self.is_falling = False
                self.is_on_ground = True

    def update(self):
        # only go through animation cycle while on ground
        if self.is_on_ground:
            self.update_animation_cycle()

        # specific frame if jumping
        else:
            self.current_frame_number = 6
            self.current_frame = self.frames[self.current_frame_number]

        self.update_jumping()

        # keep hit box centered in rect
        self.hit_box.centerx = self.rect.centerx
        self.hit_box.centery = self.rect.centery

    def draw(self, screen):
        screen.blit(self.current_frame, self.rect)
