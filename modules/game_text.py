import pygame


class GameText:
    """Text object that are easy to render in game"""

    def __init__(self, transform: pygame.math.Vector2, text: str):
        self.transform = transform
        self.text = text
        self.font_face = "Consolas"
        self.font_size = 24
        self.font_color = (255, 255, 255)
        self.sprite = pygame.font.SysFont(
            self.font_face, self.font_size).render(str(self.text), True, self.font_color)
        self.render_offset = 0

    def render(self, screen: pygame.Surface):
        """Renders the text on given screen"""
        if self.render_offset == 0:
            # No offset -> Get the center of the sprite and render it there
            sprite_transform = self.transform - \
                ((self.sprite.get_width() / 2), (self.sprite.get_height() / 2))

        elif self.render_offset != 0:
            # Offset -> Subtract the offset to the transform and render it there
            # Not calculating the center
            sprite_transform = self.transform - self.render_offset

        screen.blit(self.sprite, sprite_transform)

    def change_text(self, new_text):
        """Changes the text rendered"""
        self.text = new_text
        self.sprite = pygame.font.SysFont(
            self.font_face, self.font_size).render(str(self.text), True, self.font_color)
