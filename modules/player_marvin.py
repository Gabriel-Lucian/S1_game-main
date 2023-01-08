import pygame
from modules.collisions import Collisions
from modules.bullet import Bullet
from modules.game_text import GameText
from modules.player import Player
from modules.sprite import Sprite


class PlayerMarvin(Player):
    """Marvin!"""

    def __init__(self, transform: pygame.math.Vector2, lane_y: list):
        super().__init__(transform)
        self.health = 5

        self.lanes = [
            pygame.math.Vector2(100, lane_y[0]),
            pygame.math.Vector2(100, lane_y[1]),
            pygame.math.Vector2(100, lane_y[2]),
        ]

        self.current_lane = 1

    def jump_up(self):
        """Jumps up a lane"""
        if self.current_lane - 1 < 0:
            return

        self.current_lane -= 1
        self.lerp_target = self.lanes[self.current_lane].copy()

    def jump_down(self):
        """Jumps down a lane"""
        if self.current_lane + 1 >= len(self.lanes):
            return

        self.current_lane += 1
        self.lerp_target = self.lanes[self.current_lane].copy()

    def shoot(self, char, target_obj) -> Bullet:
        """Returns a Bullet obj that has the given target"""
        bullet = GameText(self.transform, char)
        bullet_obj = Bullet(self.transform)
        bullet_obj.sprite = Sprite([bullet.sprite])
        bullet_obj.collisions = Collisions(bullet_obj.sprite)
        bullet_obj.move_speed = 1
        bullet_obj.add_target_direction(target_obj)
        return bullet_obj

    def take_damage(self, amount):
        """Removes health or kills Marvin"""
        if self.health - amount <= 0:
            self.die()
        self.health -= amount
