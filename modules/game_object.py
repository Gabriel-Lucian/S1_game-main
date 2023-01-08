import pygame
from modules.animator import Animator
from modules.collisions import Collisions


class GameObject:
    """Object easily rendered and maipulated in the game"""

    def __init__(self, transform: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
        self.sprite = 0
        self.transform = pygame.math.Vector2(transform)
        self.animator = 0
        self.collisions = 0
        self.name = "GameObject"
        self.velocity = pygame.math.Vector2(0, 0)
        self.lerp_target = 0
        self.target_obj = 0
        self.move_speed = 5
        self.obj_list = []
        self.children = []

    def render(self, screen: pygame.Surface):
        """Renders the object to the gives screen"""
        if self.sprite != 0:
            # Getting the center of the image
            sprite_transform = self.transform - (
                (self.sprite.current().get_width() / 2),
                (self.sprite.current().get_height() / 2),
            )

            # If the object has collisions move them with the object
            if isinstance(self.collisions, Collisions):
                self.collisions.move(sprite_transform)

            # Rendering the image
            screen.blit(self.sprite.current(), sprite_transform)

        self.after_render(screen)

        # render children object
        self.render_children(screen)

    def run(self):
        """Adds movement and anumations to the object"""
        # Apply velocity
        self.translate(self.velocity)

        # Move to lerp target if there is one
        if self.lerp_target != 0:
            self.lerp(self.lerp_target, self.move_speed)

        # Run animations
        if isinstance(self.animator, Animator):
            self.animator.run(self.sprite)

        # run children objects
        self.run_children()

    def render_children(self, screen):
        """renders the children on self.children array"""
        for child in self.children:
            child[0].transform = self.transform + child[1]
            child[0].render(screen)

    def run_children(self):
        """runs the children on self.children array"""
        for child in self.children:
            if isinstance(child, GameObject):
                child.run()

    def translate(self, value: pygame.math.Vector2):
        """Adds given vector to the current position"""
        self.transform += value

    def lerp(self, target: pygame.math.Vector2, speed: float):
        """Adds a target to the object. The object will move towards it in render."""
        if self.transform.distance_to(target) <= 2:
            self.transform = target
            self.lerp_target = 0
            self.velocity = pygame.math.Vector2(0, 0)
            return

        if self.transform.distance_to(target) > 1:
            self.velocity = (
                pygame.math.Vector2(target - self.transform).normalize()
                * pygame.math.Vector2(target - self.transform).magnitude()
                * 0.01
                * speed
            )

    def add_target_direction(self, target_obj):
        """Adds a direction where the object will move with the move speed it has"""
        self.target_obj = target_obj
        target_vector = (
            pygame.math.Vector2(target_obj.transform -
                                self.transform).normalize()
            * self.move_speed
        )
        self.add_velocity(target_vector)

    def add_velocity(self, amount: pygame.math.Vector2):
        """Adds the amount given to velocity"""
        self.velocity += amount

    def add_child(self, child):
        """Adds a child to the gameobject"""
        self.children.append(
            [child, child.transform - self.transform])

    def destroy(self):
        """If the object has an obj_list it will be removed from it"""
        if self in self.obj_list:
            self.obj_list.remove(self)

    def after_render(self, screen):
        """Abstact class that is called at the end of render"""
