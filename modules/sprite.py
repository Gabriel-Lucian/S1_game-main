import pygame


class Sprite:
    """Stores a list of images as a sprite"""

    def __init__(self, images: list[pygame.Surface]) -> None:
        self.images = images
        self.index = 0

    def resize_all(self, multiplyer):
        """Resizes all images with the multiplyer given"""
        for i, img in enumerate(self.images):
            self.images[i] = pygame.transform.scale(img, (img.get_width(
            ) * multiplyer, img.get_height() * multiplyer))

    def set_size_all(self, resolution: tuple):
        """Resizes all images to the size given"""
        for i, img in enumerate(self.images):
            self.images[i] = pygame.transform.scale(img, resolution)

    def next_frame(self):
        """Changes the sprite to use the next image"""
        if (self.index + 1 < len(self.images)):
            self.index += 1
        else:
            self.index = 0

    def last_frame(self):
        """Changes the sprite to use the last image"""
        if(self.index > 0):
            self.index += 1
        else:
            self.index = len(self.images)

    def current(self) -> pygame.image:
        """Returns the current image used"""
        return self.images[self.index]

    def get_height(self):
        """Returns the height of the current image"""
        return self.current().get_height()

    def get_width(self):
        """Returns the width of the current image"""
        return self.current().get_width()
