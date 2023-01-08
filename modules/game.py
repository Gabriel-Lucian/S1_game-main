"""Marvin Game!"""
# pylint: disable=redefined-outer-name
import os
import sys
import re
from random import randint
import pygame


# Importing used modules from Modules folder
from modules.animator import Animator
from modules.asteroid import Asteroid
from modules.collisions import Collisions
from modules.game_event import GameEvents, rase_event
from modules.game_object import GameObject
from modules.game_text import GameText
from modules.health_bar import HealthBar
from modules.inteval_timer import IntervalTimer
from modules.play_sound import Sounds, play_ones
from modules.player_marvin import PlayerMarvin
from modules.text_loader import text_loader
from levels import Level
import modules.sprites as sprites
import modules.menu as menu


# DEVELOPING/TESTING
from fps_meter import display_fps
from modules.user_save import UserSave


class Game:
    """For making a game instance"""

    def __init__(self, screen: pygame.Surface, level: Level, user_save: UserSave):
        self.clock = pygame.time.Clock()

        self.level = level

        self.user_save = user_save

        # game setting
        self.max_fps = 60

        # difficulty settings
        self.word_difficulty = self.level.word_difficulty
        self.typo_penalty = self.level.typo_penalty
        self.asteroid_start_interval = self.level.asteroid_start_interval
        self.asteroid_start_velocity = self.level.asteroid_start_velocity
        self.asteroid_amount = self.level.asteroid_amount
        self.asteroid_interval_change = self.level.asteroid_interval_change
        self.asteroid_velocity_change = self.level.asteroid_velocity_change
        self.pickup_amount = self.level.pickup_amount

        self.running = True
        self.paused = False
        self.game_over = False
        self.lvl_cleared = False
        self.score = 0

        self.asteroid_timer = IntervalTimer(self.asteroid_start_interval)

        self.screen = screen
        pygame.display.set_caption("Marvin Game")

        self.word_list = {
            "easy": [],
            "medium": [],
            "hard": [],
        }

        for file in os.listdir("words"):
            content = text_loader("./words/" + file)
            self.word_list["easy"] += content["easy"]
            self.word_list["medium"] += content["medium"]
            self.word_list["hard"] += content["hard"]

        self.lanes = [200, self.screen.get_height()/2,
                      self.screen.get_height()-100]

        # Creating the hud
        hud_backing = GameObject((self.screen.get_width()/2, 50))
        hud_backing.sprite = sprites.create_rect_sprite(
            (self.screen.get_width(), 60), )
        health_bar = HealthBar(pygame.math.Vector2(
            self.screen.get_width() - 200, 50))
        lvl_name_txt = GameText(pygame.math.Vector2(
            self.screen.get_width() / 2, 50), self.level.lvl_name)
        lvl_name = GameObject(pygame.math.Vector2(
            self.screen.get_width() - 100, 50))
        lvl_name.add_child(lvl_name_txt)
        # creating the score object
        player_score_text = GameText(pygame.math.Vector2(200, 50), 0)
        player_score_text.font_size = 32
        player_score = GameObject(pygame.math.Vector2(200, 50))
        player_score.add_child(player_score_text)

        # GameObjects
        self.game_obj = {
            "game": {
                "background": [],
                "player": [],
                "bullet": [],
                "particle": [],
                "asteroid": [],
            },
            "hud": {
                "backing": hud_backing,
                "health_bar": health_bar,
                "score": player_score,
                "lvl_name": lvl_name,
            },
            "pause": [],
            "lvl_cleared": [],
            "over": [],

        }

        self.text_obj = {"all": [], "menu": [], "game": []}

        self.player = PlayerMarvin(
            pygame.math.Vector2(100, self.lanes[1]), self.lanes)
        self.player.sprite = sprites.create_player_sprite()
        self.player.animator = Animator(50)
        self.player.collisions = Collisions(self.player.sprite)
        self.player.health = self.level.start_health
        self.game_obj["game"]["player"].append(self.player)

        # background image
        self.background = GameObject(pygame.math.Vector2(
            self.screen.get_width()/2, self.screen.get_height()/2))
        self.background.sprite = sprites.create_background_sprite((
            self.screen.get_width(), self.screen.get_height()))
        self.game_obj["game"]["background"].append(self.background)

        # Creating pause menu
        self.game_obj["pause"].append(GameText(pygame.math.Vector2(
            self.screen.get_width()/2, self.screen.get_height()/2), "PAUSE MENU! (Space to continue)"))

        # create lvl_cleared screen
        self.game_obj["lvl_cleared"].append(GameText(pygame.math.Vector2(
            self.screen.get_width()/2, self.screen.get_height()/2), "lvl_cleared!"))

        # creating game over screen
        self.game_obj["over"].append(GameText(pygame.math.Vector2(
            self.screen.get_width()/2, self.screen.get_height()/2), "GAME OVER! (Space to restart)"))

        # updating the hud with correct values
        self.game_obj["hud"]["health_bar"].health = self.player.health
        self.game_obj["hud"]["health_bar"].update()

    def play(self):
        """start the game loop"""
        while self.running:
            self.event_loop()
            self.update()
            # DEBUG/DEVELOP MODE
            display_fps(self.screen, self.clock)
            # Updating whole display
            pygame.display.update()
            self.clock.tick(self.max_fps)

    def event_loop(self):
        """checks pygame events"""
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                pygame.quit()  # pylint: disable=no-member
                sys.exit()

            # In game
            if not self.game_over and not self.lvl_cleared and not self.paused:
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_UP:  # pylint: disable=no-member
                        self.player.jump_up()
                    if event.key == pygame.K_DOWN:  # pylint: disable=no-member
                        self.player.jump_down()
                    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                        self.paused = True
                    if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                        menu.menu(self.screen, self.user_save)

                    elif re.match("[A-ö]|'|,|.", event.unicode):
                        # Looping trough all the asteroids
                        shot_an_asteroid = False
                        for asteroid in self.game_obj["game"]["asteroid"]:
                            if asteroid.lane != self.player.current_lane:
                                continue

                            # Shooting at the first one with a character match
                            if asteroid.current_char() == event.unicode:
                                shot_an_asteroid = True
                                bullet = self.player.shoot(
                                    event.unicode, asteroid)

                                # Add that bullet to be collided with the asteroid
                                bullet.collisions.add_to_collide_with_list(
                                    [asteroid])
                                bullet.obj_list = self.game_obj["game"]["bullet"]

                                if len(asteroid.text) <= 1:
                                    # Last character -> add the asteroid to collide with bullet
                                    asteroid.collisions.add_to_collide_with_list([
                                        bullet])

                                self.game_obj["game"]["bullet"].append(
                                    bullet)
                                asteroid.next_character()
                                break

                        # Player misstyped
                        if not shot_an_asteroid:
                            self.score -= self.typo_penalty
                            self.screen.fill((255, 30, 30))

            # lvl_cleared events
            elif self.lvl_cleared:
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                        menu.menu(self.screen, self.user_save, "level_select")

            # game over events
            elif self.game_over:
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                        self.__init__(self.screen, self.level, self.user_save)

            # pause menu
            elif self.paused:
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                        # Continue game
                        self.paused = False

            # on player died
            if event.type == GameEvents.player_died:
                self.game_over = True
                self.game_obj["hud"]["score"].lerp_target = pygame.math.Vector2(
                    self.screen.get_width()/2, self.screen.get_height()/2)

            # on on lvl cleared
            if event.type == GameEvents.lvl_cleared:
                self.user_save.add_score(self.level.lvl_name, self.score)
                self.user_save.save()

            # on asteroid destroyed
            if event.type == GameEvents.asteroid_destroyed:
                self.score += event.sender.score
                self.game_obj["game"]["asteroid"].remove(event.sender)
                play_ones(Sounds.asteroid_explode, 0.1)

            # on asteroid hit player
            if event.type == GameEvents.asteroid_hit_player:
                self.game_obj["game"]["asteroid"].remove(event.sender)
                if not self.game_over:
                    self.player.take_damage(event.sender.dmg)
                    self.game_obj["hud"]["health_bar"].health = self.player.health
                    self.game_obj["hud"]["health_bar"].update()

            # on asteroid hit back wall
            if event.type == GameEvents.asteroid_hit_wall:
                self.game_obj["game"]["asteroid"].remove(event.sender)
                if not self.game_over:
                    self.score -= self.typo_penalty

    def update(self):
        """updates the game"""
        # Setting games bg color
        self.screen.fill((30, 30, 30))

        if not self.game_over and not self.lvl_cleared and not self.paused:
            # Rendering all gameobjects from GameObject modules list game_obj
            self.render_obj_dict(self.game_obj["game"], True)

            # rendering all text objects
            self.render_obj_dict(self.text_obj)

            # rendering the hud
            for value in self.game_obj["hud"].items():
                if value[0] == "score":
                    value[1].children[0][0].change_text(self.score)
                value[1].render(self.screen)
                value[1].run()

            for bullet in self.game_obj["game"]["bullet"]:
                if bullet.target_obj in self.game_obj["game"]["asteroid"]:
                    bullet.add_target_direction(bullet.target_obj)
                else:
                    self.game_obj["game"]["bullet"].remove(bullet)

            # spawn asteroids
            if self.asteroid_amount > 0 or self.pickup_amount > 0:
                if self.asteroid_timer.do_action():

                    if self.pickup_amount <= 0:
                        self.instantiate_asteroid()
                        self.asteroid_amount -= 1

                    elif self.asteroid_amount <= 0:
                        self.instantiate_pickup()
                        self.pickup_amount -= 1

                    elif randint(0, 3) > 0:
                        self.instantiate_asteroid()
                        self.asteroid_amount -= 1

                    else:
                        self.instantiate_pickup()
                        self.pickup_amount -= 1

                    if self.asteroid_timer.interval > 100:
                        self.asteroid_timer.interval -= self.asteroid_interval_change
                        self.asteroid_start_velocity = round(
                            self.asteroid_start_velocity + self.asteroid_velocity_change, 3)

            elif len(self.game_obj["game"]["asteroid"]) <= 0 and not self.lvl_cleared:
                self.lvl_cleared = True
                rase_event(GameEvents.lvl_cleared, self.level)

            if self.score <= -100:
                self.game_over = True

        elif self.paused:
            # rendering the hud
            for value in self.game_obj["hud"].items():
                value[1].render(self.screen)

            # Rendering all game objects
            self.render_obj_dict(self.game_obj["game"])

            # Rendering all pause objects
            self.render_obj_list(self.game_obj["pause"])

        elif self.lvl_cleared:
            # rendering the hud
            for value in self.game_obj["hud"].items():
                value[1].render(self.screen)

            # Rendering all game objects
            self.render_obj_dict(self.game_obj["game"], True)

            # Rendering all game vicotry objects
            self.render_obj_list(self.game_obj["lvl_cleared"])

        elif self.game_over:
            # rendering the hud
            for value in self.game_obj["hud"].items():
                value[1].render(self.screen)

            # Rendering all game objects
            self.render_obj_dict(self.game_obj["game"], True)

            # Rendering all game over objects
            self.render_obj_list(self.game_obj["over"])

    def render_obj_dict(self, obj_list: dict[str, GameObject], run: bool = False):
        """Renders and runs all the objects given"""
        for value in obj_list.items():
            for obj in value[1]:
                if run:
                    obj.run()
                obj.render(self.screen)

    def render_obj_list(self, obj_list: list, run: bool = False):
        """Renders and runs all the objects given"""
        for obj in obj_list:
            if run:
                obj.run()
            obj.render(self.screen)

    def get_random_word(self):
        """ "Returns a word from asteroid words that is not on the screen allready"""
        # Generate a random word from asteroid words
        new_word = self.word_list[self.word_difficulty][randint(
            0, len(self.word_list[self.word_difficulty]) - 1)]

        valid = True

        # Loop trough all of the typing objects for same words
        for obj in self.game_obj["game"]["asteroid"]:
            if obj.text == new_word:
                valid = False
                break

        # Return the word only if it is not on screen
        if valid:
            return new_word

        # Try again if the word is on screen
        return self.get_random_word()

    def instantiate_asteroid(self):
        """Spawns an asteroid with random word to a random lane"""
        random_lane = randint(0, 2)
        pos = (self.screen.get_width(), self.lanes[random_lane])
        word = self.get_random_word()
        new_asteroid = Asteroid(pos, word)
        new_asteroid.sprite = sprites.create_asteroid_sprite()
        new_asteroid.lane = random_lane
        new_asteroid.animator = Animator(2)
        new_asteroid.collisions = Collisions(new_asteroid.sprite)
        new_asteroid.collisions.add_to_collide_with_list(
            self.game_obj["game"]["player"])
        new_asteroid.velocity = pygame.math.Vector2(
            -self.asteroid_start_velocity, 0)
        self.game_obj["game"]["asteroid"].append(new_asteroid)
        play_ones(Sounds.asteroid_spawn, 0.05)

    def instantiate_pickup(self):
        """Spawns an asteroid with random word to a random lane"""
        random_lane = randint(0, 2)
        pos = (self.screen.get_width(), self.lanes[random_lane])
        word = self.get_random_word()
        new_pickup = Asteroid(pos, word)
        new_pickup.dmg = 0
        new_pickup.score = pow(len(new_pickup.text), 3)
        new_pickup.sprite = sprites.create_pickup_sprite()
        new_pickup.lane = random_lane
        new_pickup.animator = Animator(2)
        new_pickup.collisions = Collisions(new_pickup.sprite)
        new_pickup.collisions.add_to_collide_with_list(
            self.game_obj["game"]["player"])
        new_pickup.velocity = pygame.math.Vector2(
            -self.asteroid_start_velocity, 0)
        self.game_obj["game"]["asteroid"].append(new_pickup)
        play_ones(Sounds.asteroid_spawn, 0.05)


def new_game(screen: pygame.Surface, level: Level, user_save: UserSave = UserSave("Marvin")):
    """Return a new game"""
    Game(screen, level, user_save).play()
