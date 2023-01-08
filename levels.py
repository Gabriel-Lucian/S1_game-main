"""Stores all of the games levels"""


class Level:
    """For makeing levels with different difficulty"""

    def __init__(self, lvl_name: str, word_difficulty: str, asteroid_amount: int, pickup_amount: int, typo_penalty: int,
                 asteroid_start_interval: int, asteroid_start_velocity: int, start_heath: int = 5, asteroid_interval_change: int = 10,
                 asteroid_velocity_change: float = 0.05):
        self.lvl_name = lvl_name
        self.word_difficulty = word_difficulty
        self.asteroid_amount = asteroid_amount
        self.pickup_amount = pickup_amount
        self.typo_penalty = typo_penalty
        self.asteroid_start_interval = asteroid_start_interval
        self.asteroid_start_velocity = asteroid_start_velocity
        self.start_health = start_heath
        self.asteroid_interval_change = asteroid_interval_change
        self.asteroid_velocity_change = asteroid_velocity_change


# TODO customize the levels
levels = {
    0: Level(
        lvl_name="lvl 2",
        word_difficulty="easy",
        asteroid_amount=1,
        pickup_amount=1,
        typo_penalty=10,
        asteroid_start_interval=150,
        asteroid_start_velocity=1,
        start_heath=5,
        asteroid_interval_change=10,
        asteroid_velocity_change=0.05
    ),
    1: Level(
        lvl_name="lvl 3",
        word_difficulty="easy",
        asteroid_amount=3,
        pickup_amount=1,
        typo_penalty=10,
        asteroid_start_interval=150,
        asteroid_start_velocity=1,
        start_heath=5,
        asteroid_interval_change=10,
        asteroid_velocity_change=0.05
    ),
    2: Level(
        lvl_name="lvl 4",
        word_difficulty="easy",
        asteroid_amount=3,
        pickup_amount=1,
        typo_penalty=10,
        asteroid_start_interval=150,
        asteroid_start_velocity=1,
        start_heath=5,
        asteroid_interval_change=10,
        asteroid_velocity_change=0.05
    ),
    3: Level(
        lvl_name="lvl 5",
        word_difficulty="easy",
        asteroid_amount=3,
        pickup_amount=1,
        typo_penalty=10,
        asteroid_start_interval=150,
        asteroid_start_velocity=1,
        start_heath=5,
        asteroid_interval_change=10,
        asteroid_velocity_change=0.05
    ),
}


def get_level(number: int):
    """Returns given level"""
    return levels[number]
