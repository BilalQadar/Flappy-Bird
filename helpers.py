import pygame
from sprites import *
from learner import *

def load_background(image_file):
    """Loads image file in pygame"""
    image = pygame.image.load(image_file)
    return image

def is_active(event):
    """Detects if an event type is quit. Returns True or False based on whether
    the close button is being pressed"""
    if event.type == pygame.QUIT:
        return False
    else:
        return True

def keys(character,event):
    """Updates the position of sprite on screen depending on whether the UP or
    DOWN arrow key is pressed """

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            character.update_pos('UP')

        elif event.key == pygame.K_DOWN:
            character.update_pos('DOWN')

def render_pipes(speed, timer, scaling, image_list, group):
    """Renders pipe images onto the screen. Pipe objects are created after a set
    number of milliseconds. The newly formed pipe is then added to the pipes
    group"""

    if timer > scaling * (1/speed) * 1000:
        characteristics = spawn_pipe(image_list)
        if characteristics is not None:
            pipe = Enemy(characteristics[0],characteristics[1], characteristics[2])
            group.add(pipe)
            return pipe

def text_to_screen(screen, text, position, color=(0,0,0)):
    """Renders text to a screen objects in a specified color and position.
    Default font color is black"""

    size = 50
    pygame.font.init()
    text = str(text)
    font = pygame.font.SysFont('Arial', size)
    text = font.render(text, True, color)
    screen.blit(text, (position[0], position[1]))

def update_timer(timer, speed, scaling):
    """Reset timer to 0 after a specified number of milliseconds has passed"""
    if timer >  scaling * (1/speed) * 1000:
        return 0
    else:
        return timer

def detect_collision(pipe_list, character):
    """Return True or False based on whether the first pipe object in the list
    of pipes is occupying the same space as the character on screen"""

    first_pipe = pipe_list[0]
    (left_p, top_p, width_p, height_p) = first_pipe.get_rect()
    (left_c, top_c, width_c, height_c) = character.get_rect()

    #Reformatting width's to corner coordinates
    width_p += left_p
    width_c += left_c
    height_p += top_p
    height_c += top_c

    x_intersect = x_intersection(left_p, width_p, left_c, width_c)
    y_interect = y_interection(top_p, height_p, top_c, height_c)

    if x_intersect and y_interect:
        return True
    else:
        return False

def change_score(pipe_list,score,speed,pipe_speed):
    """Update score depending on the number of pipes the bird has travelled past.
    Everytime the score is updated, also update the level
    """

    updated_score = update_score(pipe_list,score)

    if updated_score is not None:
        if updated_score > score:
            pipe_speed = change_level(score,pipe_speed)

    return (updated_score,pipe_speed)