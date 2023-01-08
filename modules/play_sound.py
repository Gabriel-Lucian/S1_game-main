"""Easy soundeffects"""
import numbers
import pygame

pygame.mixer.init()  # pylint: disable=no-member


class Sounds:
    """Stores the games soundeffects"""
    space = pygame.mixer.Sound("./sounds/space-exploration-10947.mp3")
    asteroid_explode = pygame.mixer.Sound("./sounds/asteroid@explode.wav")
    asteroid_spawn = pygame.mixer.Sound("./sounds/asteroid@spawn.wav")


def play_ones(sound_effect: pygame.mixer.Sound, volume: numbers):
    """Plays the instances soundeffect ones"""
    sound_effect.set_volume(volume)
    pygame.mixer.Sound.play(sound_effect)
