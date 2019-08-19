import pygame
import sys


class Hud():
    def __init__(self, settings, screen):
        # keep track of time
        self.score = 0

        # keep track of settings
        self.settings = settings

        # keep track of screen
        self.screen = screen

        # initialize pause image
        self.pause_image = pygame.image.load('images/pause.bmp')
        self.pause_rect = self.pause_image.get_rect()
        self.pause_rect.top = 0
        self.pause_rect.left = 0

        # keep track of number of lives
        self.number_of_lives = 2

        # keep track of mode
        self.mode = 'jumping'

        # keep track of campaign funds
        self.campaign_funds = self.settings.start_campaign_funds

        # initialize campaign funds image
        self.campaign_funds_image = None

        # initialize campaign funds rectangle
        self.campaign_funds_rect = pygame.Rect(200, 440, 150, 50)

        # object that renders text
        self.font = pygame.font.SysFont('Arial', 24)

        # initializing lives label
        self.lives_label_rect = pygame.Rect(10, 410, 100, 50)
        self.lives_label_image = self.font.render('Lives:', True, self.settings.hud_text_color,
            self.settings.hud_bg_color)

        # initializing campaign funds label
        self.campaign_funds_label_rect = pygame.Rect(10, 440, 150, 50)
        self.campaign_funds_label_image = self.font.render('Campaign Funds:', True, self.settings.hud_text_color,
            self.settings.hud_bg_color)

        # initializing time label
        self.score_label_rect = pygame.Rect(200, 410, 60, 50)
        self.score_label_image = self.font.render('Score:', True, self.settings.hud_text_color,
            self.settings.hud_bg_color)

        self.player_score_rect = pygame.Rect(275, 410, 60, 50)
        self.player_score_image = self.font.render(str(self.score), True, self.settings.hud_text_color,
            self.settings.hud_bg_color)

        # load images for first and second life
        self.first_life_image = pygame.image.load('images/bernie_2016_bumper_sticker.bmp')
        self.second_life_image = pygame.image.load('images/bernie_2020_bumper_sticker.bmp')

        # set up rectangles for lives
        self.second_life_rect = self.first_life_image.get_rect()
        self.second_life_rect.top = 415
        self.second_life_rect.left = 80

        self.first_life_rect = self.second_life_image.get_rect()
        self.first_life_rect.top = 415
        self.first_life_rect.left = 135

        # load more images for hud
        self.jump_over_junk_image = pygame.image.load('images/jump_over_junk.bmp')
        self.arrow_image = pygame.image.load('images/arrow.bmp')
        self.get_funds_from_the_people_image = pygame.image.load('images/get_funds_from_the_people.bmp')

        self.jump_over_junk_rect = self.jump_over_junk_image.get_rect()
        self.jump_over_junk_rect.left = 25
        self.jump_over_junk_rect.top = 475

        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.left = 160
        self.arrow_rect.top = 515

        self.get_funds_from_the_people_rect = self.get_funds_from_the_people_image.get_rect()
        self.get_funds_from_the_people_rect.left = 265
        self.get_funds_from_the_people_rect.top = 475

        self.not_me_us_image = pygame.image.load('images/not_me_us.bmp')
        self.not_me_us_rect = self.not_me_us_image.get_rect()
        self.not_me_us_rect.left = 420
        self.not_me_us_rect.top = 415

        # load transparent bernie head
        self.bernie_head_image = pygame.image.load('images/bernie_head.bmp')

        self.bernie_head_rect_jumping = self.bernie_head_image.get_rect()
        self.bernie_head_rect_jumping.left = self.jump_over_junk_rect.left
        self.bernie_head_rect_jumping.top = self.jump_over_junk_rect.top

        self.bernie_head_rect_fundraising = self.bernie_head_image.get_rect()
        self.bernie_head_rect_fundraising.left = self.get_funds_from_the_people_rect.left
        self.bernie_head_rect_fundraising.top = self.get_funds_from_the_people_rect.top

    def draw(self):
        # draw bg of hud
        pygame.draw.rect(self.screen, self.settings.hud_bg_color,
            (0, self.settings.top_of_hud, self.settings.game_width, self.settings.hud_height))

        # draw labels of hud
        self.screen.blit(self.lives_label_image, self.lives_label_rect)
        self.screen.blit(self.campaign_funds_label_image, self.campaign_funds_label_rect)
        self.screen.blit(self.score_label_image, self.score_label_rect)

        # update score image
        self.player_score_image = self.font.render(str(self.score), True, self.settings.hud_text_color,
            self.settings.hud_bg_color)

        # draw players score
        self.screen.blit(self.player_score_image, self.player_score_rect)

        # draw lives
        if self.number_of_lives == 2:
            self.screen.blit(self.second_life_image, self.second_life_rect)
            self.screen.blit(self.first_life_image, self.first_life_rect)
        elif self.number_of_lives == 1:
            self.screen.blit(self.second_life_image, self.second_life_rect)
        elif self.number_of_lives == 0:
            pass
        else:
            print('Error: Number of Lives is ' + str(self.number_of_lives))
            sys.exit()

        # draw current campaign funds
        curr_funds = "$" +  "{:,}".format(self.campaign_funds)
        self.campaign_funds_image = self.font.render(curr_funds, True, self.settings.hud_text_color,
            self.settings.hud_bg_color)
        self.screen.blit(self.campaign_funds_image, self.campaign_funds_rect)

        # draw area that tell user whether they're jumping or fundraising
        self.screen.blit(self.jump_over_junk_image, self.jump_over_junk_rect)
        self.screen.blit(self.arrow_image, self.arrow_rect)
        self.screen.blit(self.get_funds_from_the_people_image, self.get_funds_from_the_people_rect)

        if self.mode == 'jumping':
            self.screen.blit(self.bernie_head_image, self.bernie_head_rect_jumping)
        elif self.mode == 'fundraising':
            self.screen.blit(self.bernie_head_image, self.bernie_head_rect_fundraising)
        else:
            print('Mode is ' + str(self.mode))

        #draw not me us image
        self.screen.blit(self.not_me_us_image, self.not_me_us_rect)

    def update(self):
        self.campaign_funds -= self.settings.loss_of_funds_per_loop
