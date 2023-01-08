import pygame
from modules.collisions import Collisions
from modules.game_object import GameObject


class Bullet(GameObject):
    """Character bullets for Marvin to shoot"""

    def __init__(self, transform: pygame.math.Vector2):
        super().__init__(transform)

    def after_render(self, screen):

        if isinstance(self.collisions, Collisions):

            collision_list = self.collisions.check_collisions()

            if len(collision_list) > 0:
                self.destroy()
