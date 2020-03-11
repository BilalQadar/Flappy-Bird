import pygame
from learner import *

class Player(pygame.sprite.Sprite):
    """Class for the main character which is controlled by the player """

    def __init__(self, image: str, size: int, start: tuple) -> None:
        """Constructor for player sprite. Inherits from pygame's Sprite
        class"""
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.x  = start[0]
        self.rect.y = start[1]

    def get_rect(self) -> list:
        """Returns the coordinates for the rectangle bounding box around
        the sprite object"""
        return self.rect

    def get_position(self) -> list:
        """Return the x,y coordinates for the top left corner of the sprite"""
        position = [self.rect.x,self.rect.y]
        return position

    def rotate(self,angle: int) -> None:
        """Updates the sprite's orientation by rotating the image by `angle`"""
        self.image = pygame.transform.rotate(self.image,angle)

    def update_pos(self, key: str) -> None:
        """Update the position of the sprite based on whether the up or down
        key is pressed"""
        position = self.get_position()
        new_position = move_sprite(key, position)

        if new_position is not None:
            self.rect.x = new_position[0]
            self.rect.y = new_position[1]

    def update(self) -> None:
        """Update the sprite's position on the screen"""
        new_position = sprite_down(self.get_position())

        if new_position is not None:
            if new_position[1] >= 600:
                new_position[1] = 600
            else:
                self.rect.y = new_position[1]

class Enemy(pygame.sprite.Sprite):
    """Class for the enemy character or object which is controlled by the
    player"""

    def __init__(self, image: str, size: int, start: int):
        """Constructor for player sprite. Inherits from pygame's Sprite
        class"""

        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.x  = start[0]
        self.rect.y = start[1]

    def get_rect(self) -> list:
        """Returns the coordinates for the rectangle bounding box around the
        sprite object"""

        return self.rect

    def get_position(self) -> list:
        """Return the x,y coordinates for the top left corner of the sprite"""

        position = [self.rect.x,self.rect.y]
        return position

    def update(self,pipe_speed: float) -> None:
        """Updates the sprite's position on the screen. Makes the enemy scroll
        across the screen"""

        new_position = move_pipe(self.get_position(),pipe_speed)

        if new_position is not None:
            self.rect.x = new_position[0]
