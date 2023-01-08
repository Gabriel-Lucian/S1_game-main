import pygame
import modules.sprites as sprites
from modules.game_object import GameObject


class HealthBar(GameObject):
    """Bar of objects to show the players health"""

    def __init__(self, transform: pygame.math.Vector2 = ...):
        super().__init__(transform)
        self.heart_sprite = sprites.create_heart_sprite()
        self.health = 3

    def update(self):
        """updates the health to a new amount"""
        self.children = []
        # calculating the first hearts position (dumb head no working math)
        offset = (((self.health - 1) * self.heart_sprite.get_width()) / 2) * -1
        for i in range(self.health):
            heart = GameObject()
            heart.sprite = self.heart_sprite
            heart.transform = pygame.Vector2(
                self.transform.x + (offset + self.heart_sprite.get_width() * i), self.transform.y)
            self.add_child(heart)
