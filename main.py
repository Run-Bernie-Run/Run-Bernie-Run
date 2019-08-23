import pygame
from classes.bernie import Bernie
from classes.settings import Settings
from classes.hud import Hud
from classes.headline import Headline
import sys
from random import randint
from classes.head import Head
from classes.tutorial import Tutorial


def check_events_game(hud, bernie, heads, settings):
    for event in pygame.event.get():
        # quit game if player clicks big X
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # switch to jumping
            if event.key == pygame.K_LEFT:
                hud.mode = 'jumping'
            # switch to raising money
            elif event.key == pygame.K_RIGHT:
                hud.mode = 'fundraising'
            # jump or raise money
            elif event.key == pygame.K_SPACE:
                # raise money
                if hud.mode == 'fundraising':
                    hud.campaign_funds += settings.add_funds_update
                # jump
                elif hud.mode == 'jumping' and bernie.is_on_ground:
                    bernie.is_jumping = True
                    bernie.is_on_ground = False
            elif event.key == pygame.K_RETURN:
                settings.paused = True
                pygame.mixer.music.pause()
        elif event.type == pygame.KEYUP:
            # start falling if player releases space early
            if event.key == pygame.K_SPACE and bernie.is_jumping:
                bernie.is_jumping = False
                bernie.is_falling = True
        elif event.type == game_clock_tick:
            hud.score += settings.points_per_milisecond

            # remove players invincibility
            if hud.score == bernie.invincible_until:
                bernie.is_invincible = False


def update_game(bernie, hud, headlines, heads, shit_sound_effect, secret_image, secret_rect):
    global game_over_score_image

    # update bernie object
    bernie.update()

    # update hud
    hud.update()

    for head in heads:
        head.update()

    # update headlines
    for headline in headlines:
        headline.update()

    # determine if obstacle is colliding with bernie
    for head in heads[:]:
        if pygame.Rect.colliderect(bernie.hit_box, head.rect):
            heads.remove(head)
            if bernie.is_invincible:
                pass
            elif hud.number_of_lives == 2:
                # take a life away from player
                hud.number_of_lives -= 1
                shit_sound_effect.play()

                 # make bernie invincible for a short period of time
                bernie.is_invincible = True
                bernie.invincible_until = hud.score + settings.invincibility_frames
            elif hud.number_of_lives == 1:
                pygame.mixer.music.stop()
                damn_sound_effect = pygame.mixer.Sound('sound_effects/damn.wav')
                damn_sound_effect.play()
                pygame.time.set_timer(game_clock_tick, 0)

                if hud.score >= settings.unlock_score:
                    screen.blit(secret_image, secret_rect)
                    pygame.display.flip()
                    pygame.time.delay(20000)

                settings.mode = 'game over'
                game_over_score_image = game_over_font.render(str(hud.score), True, RED, LIGHT_BLUE)
            else:
                raise Exception('Number of lives is ' + str(hud.number_of_lives))

    if hud.campaign_funds <= 0:
        pygame.mixer.music.stop()
        damn_sound_effect = pygame.mixer.Sound('sound_effects/damn.wav')
        damn_sound_effect.play()
        pygame.time.set_timer(game_clock_tick, 0)

        if hud.score >= settings.unlock_score:
            screen.blit(secret_image, secret_rect)
            pygame.display.flip()
            pygame.time.delay(20000)

        settings.mode = 'game over'
        game_over_score_image = game_over_font.render(str(hud.score), True, RED, LIGHT_BLUE)

    # remove headline is its off screen
    for headline in headlines[:]:
        if headline.is_off_screen:
            headlines.remove(headline)
            headlines.append(Headline(500, screen, settings))

    # remove obstacles that are off screen
    for head in heads[:]:
        if head.is_off_screen:
            heads.remove(head)

    # spawn obstacles
    if hud.score > settings.last_spawn_time + settings.spawn_rate:
        # give last spawn time new value
        settings.last_spawn_time = hud.score

        # randomly generate one of eight obstacles
        obstacle_num = randint(1, 8)

        if obstacle_num == 1:
            heads.append(Head(settings, 340, screen, 1))
        elif obstacle_num == 2:
            heads.append(Head(settings, 280, screen, 1))
        elif obstacle_num == 3:
            heads.append(Head(settings, 340, screen, 2))
        elif obstacle_num == 4:
            heads.append(Head(settings, 280, screen, 2))
        elif obstacle_num == 5:
            heads.append(Head(settings, 340, screen, 1))
            heads.append(Head(settings, 280, screen, 1))
        elif obstacle_num == 6:
            heads.append(Head(settings, 340, screen, 1, 660))
            heads.append(Head(settings, 340, screen, 1, 720))
        elif obstacle_num == 7:
            heads.append(Head(settings, 280, screen, 1, 660))
            heads.append(Head(settings, 340, screen, 1, 720))
        elif obstacle_num == 8:
            heads.append(Head(settings, 340, screen, 1, 660))
            heads.append(Head(settings, 280, screen, 1, 720))


def draw_game(bernie, hud, headlines, heads):
    # fill screen with white
    screen.fill((255, 255, 255))

    # draw headlines
    for headline in headlines:
        headline.draw()

    # draw bernie
    bernie.draw(screen)

    for head in heads:
        head.draw()

    # draw hud
    hud.draw()

    # update screen
    pygame.display.flip()


def paused(settings, hud, screen, bernie):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                settings.paused = False
                pygame.mixer.music.unpause()
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                bernie.is_jumping = False
                bernie.is_falling = True

    # draw pause screen
    screen.blit(hud.pause_image, hud.pause_rect)
    pygame.display.flip()


def check_event_title(settings, sound_effects, get_ready_image, get_ready_rect):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                settings.selector = 'tutorial'
            elif event.key == pygame.K_UP:
                settings.selector = 'play'
            if event.key == pygame.K_RETURN:
                if settings.selector == 'play':
                    settings.last_spawn_time = 0
                    settings.mode = 'game'

                    # start timers
                    pygame.time.set_timer(game_clock_tick, 1)

                    # start music
                    pygame.mixer.music.load('music/superman.ogg')
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)

                    # create bernie object
                    bernie = Bernie(settings)

                    # create hud object
                    hud = Hud(settings, screen)

                    # create headlines
                    headlines = [Headline(0, screen, settings),
                                Headline(100, screen, settings),
                                Headline(200, screen, settings),
                                Headline(300, screen, settings),
                                Headline(400, screen, settings),
                                Headline(500, screen, settings)]

                    # create list for heads
                    heads = []

                    # play random sound effect
                    sound_effect_num = randint(0, settings.num_sound_effects - 1)
                    delay_length = int(sound_effects[sound_effect_num].get_length()) * 1000
                    delay_length += 1500
                    sound_effects[sound_effect_num].play()

                    # display get ready screen
                    screen.blit(get_ready_image, get_ready_rect)
                    pygame.display.flip()
                    pygame.time.delay(delay_length)

                    return (bernie, hud, headlines, heads)
                elif settings.selector == 'tutorial':
                    settings.mode = 'tutorial'

        elif event.type == pygame.QUIT:
            sys.exit()

    return None, None, None, None


def draw_title(title_screen_image, title_screen_rect, selector_image, selector_rect_play,
    selector_rect_tutorial, title_bernie):
    # draw title screen
    screen.blit(title_screen_image, title_screen_rect)

    if settings.selector == 'play':
        screen.blit(selector_image, selector_rect_play)
    elif settings.selector == 'tutorial':
        screen.blit(selector_image, selector_rect_tutorial)

    title_bernie.draw(screen)

    pygame.display.flip()


def run_game():
    #game objects
    bernie = None
    hud = None
    headlines = None
    heads = None

    # start music
    pygame.mixer.music.load('music/power_to_the_people.ogg')
    pygame.mixer.music.play(-1)

    # initialize title screen image and rectangle
    title_screen_image = pygame.image.load('images/title_screen.bmp')
    title_screen_rect = title_screen_image.get_rect()
    title_screen_rect.top = 0
    title_screen_rect.left = 0

    # load selector
    selector_image = pygame.image.load('images/selector.bmp')

    # initialize title bernie
    title_bernie = Bernie(settings)
    title_bernie.rect.left = 400
    title_bernie.rect.top = 400

    selector_rect_play = selector_image.get_rect()
    selector_rect_play.top = 472
    selector_rect_play.left = 10

    selector_rect_tutorial = selector_image.get_rect()
    selector_rect_tutorial.top = 507
    selector_rect_tutorial.left = 10

    # load shit sound effect
    shit_sound_effect = pygame.mixer.Sound('sound_effects/shit.wav')
    shit_sound_effect.set_volume(0.8)

    # load other sound effects
    sound_effects = [pygame.mixer.Sound('sound_effects/i_wrote_the_damn_bill.ogg'),
                     pygame.mixer.Sound('sound_effects/health_care_is_a_human_right.ogg'),
                     pygame.mixer.Sound('sound_effects/we_have_more_people_in_jail.ogg'),
                     pygame.mixer.Sound('sound_effects/three_billionaires.ogg'),
                     pygame.mixer.Sound('sound_effects/more_than_the_next_ten_countries.ogg'),
                     pygame.mixer.Sound('sound_effects/should_not_be_living_in_poverty.ogg'),
                     pygame.mixer.Sound('sound_effects/if_a_bank_is_too_big_to_fail.ogg'),
                     pygame.mixer.Sound('sound_effects/bottom_on_up.ogg'),
                     pygame.mixer.Sound('sound_effects/us_not_me.ogg'),
                     pygame.mixer.Sound('sound_effects/amazon_pays_zero.ogg')]

    sound_effects[1].set_volume(0.5)

    # initialize get ready screen
    get_ready_image = pygame.image.load('images/get_ready.bmp')
    get_ready_rect = get_ready_image.get_rect()
    get_ready_rect.left = 0
    get_ready_rect.top = 0

    # images for game over screen
    game_over_image = pygame.image.load('images/game_over.bmp')
    game_over_rect = game_over_image.get_rect()
    game_over_rect.top = 0
    game_over_rect.left = 0

    game_over_headline_image = pygame.image.load('images/headlines/400x68/headline' + str(randint(1, 20))
        + '.bmp')
    game_over_headline_rect = game_over_headline_image.get_rect()
    game_over_headline_rect.top = 435
    game_over_headline_rect.left = 120

    # create tutorial object
    tutorial = Tutorial(screen, settings)

    # load secret
    secret_image = pygame.image.load('images/secret.bmp')
    secret_rect = secret_image.get_rect()
    secret_rect.top = 0
    secret_rect.left = 0

    # game loop
    while True:
        if settings.mode == 'title':
            bernie, hud, headlines, heads = check_event_title(settings, sound_effects, get_ready_image, get_ready_rect)
            if settings.mode == 'title':
                draw_title(title_screen_image, title_screen_rect, selector_image, selector_rect_play,
                    selector_rect_tutorial, title_bernie)
                title_bernie.update()
        elif settings.mode == 'game':
            if not settings.paused:
                check_events_game(hud, bernie, heads, settings)
                generate_score_image = update_game(bernie, hud, headlines, heads, shit_sound_effect, secret_image, secret_rect)
                draw_game(bernie, hud, headlines, heads)
            else:
                paused(settings, hud, screen, bernie)
        elif settings.mode == 'game over':
            # draw background
            screen.blit(game_over_image, game_over_rect)
            screen.blit(game_over_headline_image, game_over_headline_rect)
            screen.blit(game_over_score_image, game_over_score_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # go back to settings
                        settings.mode = 'title'

                        # start title music
                        pygame.mixer.music.load('music/power_to_the_people.ogg')
                        pygame.mixer.music.play(-1)

                        # load headline for next time
                        game_over_headline_image = pygame.image.load('images/headlines/400x68/headline'
                            + str(randint(1, 20)) + '.bmp')
        elif settings.mode == 'tutorial':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        tutorial.update()

            if settings.mode == 'tutorial':
                tutorial.draw()

        clock.tick(settings.FPS)


# initialize pygame
pygame.init()
pygame.display.set_caption('Run, Bernie, Run!')
screen = pygame.display.set_mode((600, 600))

# set up pygame icon
icon = pygame.image.load('images/bernie_icon.bmp')
pygame.display.set_icon(icon)

# create global objects
settings = Settings()
clock = pygame.time.Clock()

# game over background color
LIGHT_BLUE = (0, 121, 214)
RED = (255, 0, 0)

# declare event types
game_clock_tick = pygame.USEREVENT + 2

# score image
game_over_font = pygame.font.SysFont('Arial Black', 32)
game_over_score_image = game_over_font.render('4200', True, RED, LIGHT_BLUE)
game_over_score_rect = game_over_score_image.get_rect()
game_over_score_rect.left = 330
game_over_score_rect.top = 330

run_game()
