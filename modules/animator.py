from modules.inteval_timer import IntervalTimer
from modules.sprite import Sprite


class Animator:
    """For adding animations to a GameObject"""

    def __init__(self, animation_speed: float):
        self.animate = True
        self.animation_speed = animation_speed
        self.animation_timer = IntervalTimer(animation_speed)
        self.animation_index = 0
        self.clock = 0

    def run(self, sprite: Sprite):
        """Plays the animation if the interval given has passed"""
        if self.animate is False:
            return

        if self.animation_timer.do_action():
            sprite.next_frame()
