import pygame
import modules.game_event as game_event
from modules.game_object import GameObject


class Player(GameObject):
    """Base Player class to create different players from"""

    def __init__(self, transform: pygame.math.Vector2):
        super().__init__(transform)
        self.is_alive = True

    def after_render(self, screen):
        pass

    def die(self):
        """Rases player_died event and changes is_alive to False"""
        self.is_alive = False
        game_event.rase_event(game_event.GameEvents.player_died, self)
