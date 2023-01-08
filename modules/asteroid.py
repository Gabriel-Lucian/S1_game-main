import pygame
from modules.collisions import Collisions
import modules.game_event as game_event
from modules.game_object import GameObject
from modules.game_text import GameText
from modules.player import Player
from modules.sprites import create_backing_sprite


class Asteroid(GameObject):
    """Asteroid object"""

    def __init__(self, transform: pygame.math.Vector2, text: str,):
        super().__init__(transform)
        self.text = text
        self.text_obj = GameText(self.transform, self.text)
        self.over_text_obj = GameText(self.transform, "")
        self.over_text_obj.font_color = (0, 255, 0)
        self.over_text_obj.render_offset = (
            self.text_obj.sprite.get_width() / 2, self.text_obj.sprite.get_height() / 2)
        self.backing_obj = GameObject(self.transform)
        self.backing_obj.sprite = create_backing_sprite((
            self.text_obj.sprite.get_width() * 1.5, self.text_obj.sprite.get_height() * 1.5))
        self.lane = 0
        self.dmg = 1
        self.score = pow(len(self.text), 2)

        self.add_child(self.backing_obj)
        self.add_child(self.text_obj)
        self.add_child(self.over_text_obj)

    def after_render(self, screen):
        if isinstance(self.collisions, Collisions):

            collision_list = self.collisions.check_collisions()

            for collision in collision_list:
                if isinstance(collision.obj, Player):
                    game_event.rase_event(
                        game_event.GameEvents.asteroid_hit_player, self)

            if len(collision_list) > 0:
                # This is the last character of this asteroid
                if len(self.text) <= 0:
                    # Destroy the bullet and destroy the asteroid
                    game_event.rase_event(
                        game_event.GameEvents.asteroid_destroyed, self)

            # If the asteroid is hitting the back wall
            if self.transform[0] <= 0:
                # Destroy the bullet and destroy the asteroid
                game_event.rase_event(
                    game_event.GameEvents.asteroid_hit_wall, self)

    def current_char(self):
        """Returns the character to type next"""
        if len(self.text) > 0:
            return self.text[0]

    def next_character(self):
        """Highlights the next character and removes first from the text"""
        self.over_text_obj.change_text(
            self.over_text_obj.text + self.text[0]
        )
        self.text = self.text[1:]
