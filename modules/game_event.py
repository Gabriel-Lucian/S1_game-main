"""Stores user made events and can be used to rase them"""
# pylint: disable=no-member
import pygame


class GameEvents:
    """List of user made game events"""
    player_died = pygame.USEREVENT + 0
    asteroid_destroyed = pygame.USEREVENT + 1
    asteroid_hit_wall = pygame.USEREVENT + 2
    asteroid_hit_player = pygame.USEREVENT + 3
    lvl_cleared = pygame.USEREVENT + 4


def rase_event(event: GameEvents, sender):
    """Rases an event"""
    pygame.event.post(pygame.event.Event(event, {"sender": sender}))
