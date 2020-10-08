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

    ### CONSTANTS ###
    scaling = 1
    pipe_speed = 7
    timer = 0
    key_timer = 0
    speed = 1
    score = 0

    ### SOUNDS ###
    game_audio = get_game_audio()
    over_audio = get_gameover_audio()

    ### FONTS ###
    size = 100
    smaller_size = 50
    pygame.font.init()
    font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", size)
    smaller_font = pygame.font.Font("./assets/fonts/ARCADECLASSIC.TTF", smaller_size)

    ### DIRECTORY NAMES & START STATES ###
    dir_name = os.path.dirname(__file__)
    is_game_over = False
    active = True
    pipe_list = []
    pipe_images = ["assets/images/pipe.png",
                   "assets/images/pipe_upside_down.png"]

    if game_audio is not None:
        game_music_file = os.path.join(dir_name,game_audio)
    if over_audio is not None:
        game_over_sound = os.path.join(dir_name,over_audio)

    ### PYGAME INITILIZATIONS ###
    pygame.display.init()
    pygame.mixer.init()
    time = pygame.time.Clock()

    #DO NOT CHANGE THE DISPLAY SET MODE
    screen = pygame.display.set_mode((700,700))

    ### SET CAPTION FOR GAME ###
    caption = set_name()
    if caption is not None:
        pygame.display.set_caption(caption)
    background_image = get_background()
    gameover_image = get_gameover_background()

    ###LOAD BACKGROUND IMAGE AND GAME OVER BACKGROUND###
    if background_image is not None:
        background = load_background(os.path.join(dir_name,background_image))
    if gameover_image is not None:
        game_over_background = load_background(os.path.join(dir_name,
                                                            gameover_image))

    PLAYER = pygame.sprite.Group()
    PIPES = pygame.sprite.Group()

    ### LOAD MAIN GAME SOUNDS ###
    if game_audio is not None:
        pygame.mixer.music.load(game_music_file)
        pygame.mixer.music.play(-1)

    ### RENDER CHARACTER ###
    character_image = get_character()
    if character_image is not None:
        character = Player(os.path.join(dir_name,character_image),(100,100),
                           (0,300))
        PLAYER.add(character)

    ######################
    ### MAIN GAME LOOP ###
    ######################

    while active and not is_game_over:

        events = pygame.event.get()
        key_pressed = False

        for event in events:
            active = is_active(event)
            if character_image is not None:
                key_pressed = keys(character, event)

        if key_pressed is False and key_timer % 5 == 0:
            PLAYER.update()
            key_timer += 1
        else:
            key_timer += 1

        new_render = render_pipes(speed, timer, scaling, pipe_images, PIPES)

        if new_render is not None:
            pipe_list.append(new_render)

        score, pipe_speed = change_score(pipe_list, score, speed, pipe_speed)

        if len(pipe_list) > 0:
            is_game_over = detect_collision(pipe_list, character)

        elif event.type == pygame.QUIT:
            is_game_over = False
            active = False
            quitGame(pygame)

        timer = update_timer(timer,speed,scaling)
        # Update everything seen on screen
        PIPES.update(pipe_speed)
        # Push background image to screen
        if background_image is not None:
            screen.blit(background, [0,0])
        # Draw player image onto screen
        PLAYER.draw(screen)
        # Draw pipe images onto screen
        PIPES.draw(screen)
        # Draw score on screen
        if score is not None:
            text_to_screen(screen, font, str(score), (700/2,50),(255,255,255))

        if active:
            pygame.display.flip()
            # Update timer to new time
            timer += time.tick()

    if is_game_over:
        # Play game over sound
        if over_audio is not None:
            pygame.mixer.music.load(game_over_sound)
            pygame.mixer.music.play(-1)

        # Remove game from screen & switch to game over background
        PIPES.remove()
        character.kill()
        screen.blit(game_over_background, [0, 0])

        while active:
            events = pygame.event.get()

            for event in events:
                active = is_active(event)
            if score is not None:
                text_to_screen(screen, smaller_font, "FINAL SCORE " + str(score),
                    (200, 600), (255, 255, 255))

            pygame.display.flip()

        quitGame(pygame)
