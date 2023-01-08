"""For starting the game"""
from modules.menu import menu
from modules.user_save import UserSave

import pygame


def main():
    """Starts the game menu"""
    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode(
        (1280, 720))
    user_save = UserSave("Marvin")
    menu(screen, user_save)


if __name__ == "__main__":
    main()
