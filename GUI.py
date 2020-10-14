import pygame
from sprites import *
from learner import *
from helpers import *
import os

def game_loop() -> None:
    """This is the main loop responsible for rendering a pygame window. This
    loop also carries out all major game logic. Many learner functions are
    called in this loop. See if you can see some of the ones you have written!
    """

    ### PYGAME INITALIZATIONS ###
    pygame.display.init()
    pygame.mixer.init()
    time = pygame.time.Clock()
    screen = pygame.display.set_mode((700,700))

    ### CONSTANTS ###
    scaling = 1
    pipe_speed = 7
    timer = 0
    key_timer = 0
    score = 0

    ### SOUNDS ###
    game_audio = get_game_audio()
    over_audio = get_gameover_audio()

    ### BACKGROUNDS & CHARACTERS ###
    background_image = get_background()
    gameover_image = get_gameover_background()
    character_image = get_character()

    ### GAME CAPTION ###
    caption = set_name()

    ### FONTS ###
    size = 100
    smaller_size = 50
    pygame.font.init()
    font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", size)
    smaller_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", smaller_size)

    ### DIRECTORY NAMES & START STATES ###
    dir_name = os.path.dirname(__file__)
    game_over = False
    active = True
    pipe_list = []
    pipe_images = ["assets/images/pipe.png",
                   "assets/images/pipe_upside_down.png"]

    if game_audio is not None:
        game_music_file = os.path.join(dir_name,game_audio)
    if over_audio is not None:
        game_over_sound = os.path.join(dir_name,over_audio)

    if background_image is not None:
        background = load_background(os.path.join(dir_name,background_image))

    if gameover_image is not None:
        game_over_background = load_background(os.path.join(dir_name,
                                                            gameover_image))
    if caption is not None:
        pygame.display.set_caption(caption)

    ### LOAD MAIN GAME SOUNDS ###
    if game_audio is not None:
        pygame.mixer.music.load(game_music_file)
        pygame.mixer.music.play(-1)

    ### RENDER CHARACTER ###
    PLAYER = pygame.sprite.Group()
    PIPES = pygame.sprite.Group()

    if character_image is not None:
        character = Player(os.path.join(dir_name,character_image),(100,100),
                           (0,300))
        PLAYER.add(character)
    else:
        character = None

    ### MAIN GAME LOOP ###
    while active and not game_over:
        key_pressed = False
        events = pygame.event.get()
        active = is_active(events)

        if not active:
            break

        new_render = render_pipes(timer, scaling, pipe_images, PIPES)
        score, pipe_speed = change_score(pipe_list, score,pipe_speed)

        if character is not None:
            key_pressed = keys(character, events)

        if key_pressed is False and key_timer % 5 == 0:
            PLAYER.update()
            key_timer += 1
        else:
            key_timer += 1

        if new_render is not None:
            pipe_list.append(new_render)

        if len(pipe_list) > 0:
            game_over = detect_collision(pipe_list, character)
            if game_over:
                break

        timer = update_timer(timer,scaling)
        # Update everything seen on screen
        PIPES.update(pipe_speed)
        # Push background image to screen
        if background_image is not None:
            screen.blit(background, [0,0])
        if score is not None:
            text_to_screen(screen, font, str(score), (700/2,50),(255,255,255))
        # Draw player image onto screen
        PLAYER.draw(screen)
        # Draw pipe images onto screen
        PIPES.draw(screen)

        if time.get_fps() > 0:
            # Update speed of pipes depending on computer framerate
            scaling = 55/time.get_fps()

        # Update timer to new time
        timer += time.tick()
        pygame.display.flip()

    if game_over:
        # Play game over sound
        if over_audio is not None:
            pygame.mixer.music.load(game_over_sound)
            pygame.mixer.music.play(-1)

        # Remove game from screen & switch to game over background
        PIPES.remove()
        if character is not None:
            character.kill()

        if game_over_background is not None:
            screen.blit(game_over_background, [0, 0])

        if score is not None:
            text_to_screen(screen, smaller_font, "FINAL SCORE IS " + str(score),
                (170, 600), (255, 255, 255))

        while active:
            events = pygame.event.get()
            active = is_active(events)
            pygame.display.flip()

    pygame.font.quit()
    pygame.mixer.quit()
    pygame.display.quit()
    pygame.quit()
