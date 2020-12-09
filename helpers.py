import pygame
from sprites import *
from learner import *


def load_background(image_file: str) -> None:
	"""Loads image file in pygame"""
	image = pygame.image.load(image_file).convert_alpha()
	return image


def remove_old_pipes(pipe_list: list) -> list:
	"""Remove the pipes which have gone off the screen 
	Predcondition: The oldest pipe is at index 0"""
	if len(pipe_list) > 0:
		position = pipe_list[0].get_rect()
		if position[0] < 0:
			pipe_list.pop(0)

	return pipe_list


def is_active(events) -> bool:
	"""Detects if an event type is quit. Returns True or False based on whether the close button is being pressed"""
	for event in events:
		if event.type == pygame.QUIT:
			return False
	return True


def keys(character: Player, events) -> bool:
	"""Updates the position of sprite on screen depending on whether the UP or
	DOWN arrow key is pressed """
	for event in events:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				character.update_pos('UP')
				return True

			elif event.key == pygame.K_DOWN:
				character.update_pos('DOWN')
				return True

			elif event.key == pygame.K_LEFT:
				character.update_pos('LEFT')
				return True

			elif event.key == pygame.K_RIGHT:
				character.update_pos('RIGHT')
				return True
	return False


def render_pipes(image_list: list, group: pygame.sprite.Group) -> Enemy:
	"""Renders pipe images onto the screen. Pipe objects are created after a set
	number of milliseconds. The newly formed pipe is then added to the pipes
	group"""
	milliseconds = pygame.time.get_ticks()
	if milliseconds % 1500 < 15: 
		characteristics = spawn_pipe(image_list)
		if characteristics is not None:
			pipe = Enemy(characteristics[0],characteristics[1], characteristics[2])
			group.add(pipe)
			return pipe


def text_to_screen(screen: pygame.display, font, text: str, position: tuple, color=(0, 0, 0)) -> None:
	"""Renders text to a screen objects in a specified color and position.
	Default font color is black and default size is 100px"""

	text = font.render(text, True, color)
	screen.blit(text, (position[0], position[1]))


def detect_collision(pipe_list: list, character: Player) -> bool:
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


def change_score(pipe_list: list, score: int, pipe_speed: int) -> tuple:
	"""Update score depending on the number of pipes the bird has travelled
	past. Every time the score is updated, also update the level
	"""
	updated_score = update_score(pipe_list, score)

	if updated_score is not None:
		if updated_score > score:
			pipes = change_level(score, pipe_speed)
			if pipes is not None:
				pipe_speed = pipes

	return (updated_score, pipe_speed)
