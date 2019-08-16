import pygame

class Settings():
    def __init__(self):
        # bernie settings
        self.bernie_height = 120
        self.bernie_width = 120
        self.bernie_start_bottom = 400
        self.bernie_left = 50
        self.bernie_jump_update = 16
        self.bernie_max_height_of_top = 0
        self.invincibility_frames = 60

        # game settings
        self.FPS = 30
        self.spawn_rate = 2500
        self.loss_of_funds_per_loop = 125000
        self.points_per_milisecond = 1
        self.paused = False
        self.last_spawn_time = pygame.time.get_ticks()
        self.time_elapsed_since_last_spawn = 0
        self.add_funds_update = 1000000
        self.mode = 'title'
        self.selector = 'play'
        self.unlock_score = 12000

        # hud settings
        self.top_of_hud = 400
        self.hud_height = 200
        self.hud_bg_color = (0, 0, 0)
        self.hud_text_color = (255, 255, 255)
        self.start_campaign_funds = 10000000

        # game window settings
        self.game_width = 600
        self.game_height = 600

        # headlines settings
        self.number_of_headlines = 20
        self.headline_scroll_speed = 1

        # heads settings
        self.number_of_heads = 17
        self.length_of_head = 60
        self.speed_of_heads_x = 8
        self.speed_of_heads_y = 4

        # sound effects settings
        self.num_sound_effects = 10
