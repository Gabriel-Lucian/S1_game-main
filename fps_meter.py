import pygame


def display_fps(screen, clock):
    "Renders the fonts as passed from display_fps"
    text_to_show = pygame.font.SysFont("Arial", 24).render(
        str(int(clock.get_fps())), 0, pygame.Color("white"))
    screen.blit(text_to_show, (10, 10))
