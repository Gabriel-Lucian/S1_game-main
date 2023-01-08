"""Creates sprites for the game"""
from random import randint
import pygame

from modules.sprite import Sprite


def create_player_sprite() -> Sprite:
    """Creates and return a player sprite"""
    player = Sprite(
        [
            pygame.image.load("img/marvin.png")
        ]
    )
    player.resize_all(0.2)
    return player


def create_asteroid_sprite() -> Sprite:
    """Creates and return an asteroid sprite"""
    colors = ["blue", "green", "orange", "pink", "yellow"]
    asteroid = Sprite(
        [pygame.image.load(f"img/planet_{colors[randint(0, len(colors) - 1)]}.png")])
    asteroid.set_size_all((100, 100))
    for i in range(180):
        asteroid.images.append(
            pygame.transform.rotate(asteroid.images[0], i * 2))
    return asteroid


def create_pickup_sprite() -> Sprite:
    """Creates and return an asteroid sprite"""
    pickup = Sprite([pygame.image.load("img/star.png")])
    for i in range(180):
        pickup.images.append(
            pygame.transform.rotate(pickup.images[0], i * 2))
    return pickup


def create_heart_sprite() -> Sprite:
    """Creates and return a heart sprite"""
    heart = Sprite([pygame.image.load("img/heart.png")])
    heart.set_size_all((50, 50))
    return heart


def create_backing_sprite(size: tuple) -> Sprite:
    """Creates and return a backing sprite"""
    backing = Sprite([pygame.image.load("img/backing.png")])
    backing.set_size_all(size)
    return backing


def create_background_sprite(size: tuple) -> Sprite:
    """Creates the background"""
    background = Sprite([pygame.image.load("img/planet_background.png")])
    background.set_size_all(size)
    return background


def create_rect_sprite(size: tuple, color: str = "purple") -> Sprite:
    """Creates colored rect sprite"""
    rect = Sprite([pygame.image.load(f"img/{color}_pixel.png")])
    rect.set_size_all(size)
    return rect
