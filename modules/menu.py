import pygame
import pygame_menu

import levels

from modules.game import new_game
from modules.user_save import UserSave

pygame.mixer.init()

bg_img = pygame_menu.BaseImage(image_path=format('img/galaxy_background.jpg'))
keyboard_img = pygame_menu.BaseImage(
    image_path=format('img/marvin_keyboard_v3.jpg'))


# Default theme settings for our menu
THEME_mytheme = pygame_menu.Theme(
    background_color=bg_img,  # transparent background
    title_background_color=(0, 0, 0, 0),
    title_font_shadow=True,
    widget_padding=15,
    widget_font_color=(255, 0, 255),
    widget_font_shadow=True,
    selection_color=(124, 252, 0),
    cursor_color=(124, 252, 0),
    title_font_color=(255, 0, 255),
    widget_background_color=(0, 0, 0, 50)
)

# Constants and global variables
FPS = 60
#WINDOW_SIZE = (1200, 700)


def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """

    bg_img = pygame.image.load('img/galaxy_background.jpg')
    bg_img = pygame.transform.scale(bg_img, (1200, 720))
    surface.blit(bg_img, (0, 0))


def update_background_music(value: tuple, enabled: bool):

    if enabled:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def menu(screen: pygame.Surface, user_save: UserSave, start_screen: str = "start"):
    """
    Main program.
    :param test: Indicate function is being tested
    """
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    # global main_menu
    # global sound
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    # surface = create_example_window('Example - Multi Input', WINDOW_SIZE)
    surface = screen
    clock = pygame.time.Clock()

    # Load background sound
    pygame.mixer.music.load('sounds/space-exploration-10947.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0)

    # Own theme here
    menu_mytheme = THEME_mytheme
    menu_mytheme.widget_font = pygame_menu.font.FONT_NEVIS
    menu_mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
    menu_mytheme.title_font = pygame_menu.font.FONT_8BIT
    menu_mytheme.title_font_size = 45
    menu_mytheme.align = pygame_menu.locals.ALIGN_CENTER
    menu_mytheme.widget_selection = pygame_menu.widgets.HighlightSelection
    #menu_mytheme.widget_font_size = 30
    menu_mytheme.widget_background_inflate = (0, 0)
    menu_mytheme.widget_font_antialias = True

    # -------------------------------------------------------------------------
    # Create menus: Rules
    # -------------------------------------------------------------------------
    rules_mytheme = THEME_mytheme
    rules_mytheme.title_offset = (470, 0)
    rules_mytheme.widget_font_size = 25
    rules_mytheme.widget_background_color = (0, 0, 0, 100)

    rules_menu = pygame_menu.Menu(
        height=screen.get_height(),
        theme=rules_mytheme,
        title='Rules',
        width=screen.get_width()
    )

    rules_menu.add.label(
        "The aim of the game is to type the words correctly and"
        "avoid getting hit by asteroids which are coming towards Marvin"
        "\n"
        "At the start of each level, you will have 5 lives to get as far as you can."
        "There are 9 levels in total with each level increasing in difficulty."
        "To win the game you will need to finish all the levels!\n"
        "\n"
        "To be able to type the word Marvin will need to be in the same line as the incoming asteroid.\n"
        "\n"
        "If you spell the word correctly, Marvin will shoot the asteroid and you will win points. Once you achieve XX points you will unlock the next level.\n"
        "\n"
        "If you make a typo, you will need to quickly type the word correctly before the asteroid hits Marvin!\n"
        "\n"
        "If Marvin gets hit, you will lose 1 life. If the asteroid goes past Marvin and you didn't finish spelling the word or completely missed it, you will lose XX points.\n"
        "\n"
        "If Marvin loses all his lives, it's game over!",
        max_char=80, margin=(0, 2),
        align=pygame_menu.locals.ALIGN_CENTER
    )
    rules_menu.add.vertical_margin(20)
    rules_menu.add.button('Back', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Controls
    # -------------------------------------------------------------------------
    controls_mytheme = THEME_mytheme
    controls_mytheme.title_offset = (410, 0)
    controls_mytheme.widget_font_size = 25

    controls_menu = pygame_menu.Menu(
        height=screen.get_height(),
        theme=controls_mytheme,
        title='Controls',
        width=screen.get_width()
    )

    controls_menu.add.label(
        "To move around in the game, you will be using your keyboard.\n"
        "\n"
        "The arrow keys will move you: "
        "Up is the up arrow & down is the down arrow\n"
        "\n"
        "The letters from A - Z: "
        "Will be used to write the words & shoot asteroids.\n"
        "\n"
        "The spacebar: "
        "Will pause the game\n"
        "\n"
        "The escape key: "
        "Pressing esc will return to menu",
        max_char=80, margin=(0, 2)
    )
    controls_menu.add.vertical_margin(20)
    controls_menu.add.image(keyboard_img)
    controls_menu.add.button('Back', pygame_menu.events.BACK)
    # -------------------------------------------------------------------------
    # Create menus: Options
    # -------------------------------------------------------------------------
    options_mytheme = THEME_mytheme
    options_mytheme.title_offset = (450, 70)
    options_mytheme.widget_font_size = 30

    options_menu = pygame_menu.Menu(
        height=screen.get_height(),
        theme=options_mytheme,
        title='Options',
        width=screen.get_width()
    )

    options_menu.add.button('Rules', rules_menu)
    options_menu.add.button('Controls', controls_menu)
    options_menu.add.selector(
        'Music ', [('On', True), ('Off', False)], onchange=update_background_music)
    options_menu.add.selector(
        'Music ', [('On', True), ('Off', False)], onchange=update_background_music)

    options_menu.add.button(
        'Return to main menu',
        pygame_menu.events.BACK,
        align=pygame_menu.locals.ALIGN_CENTER
    )

    # -------------------------------------------------------------------------
    # Create menus: level select
    # -------------------------------------------------------------------------

    level_select_menu = pygame_menu.Menu(
        height=screen.get_height(),
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=menu_mytheme,
        title='Levels',
        width=screen.get_width()
    )

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    menu_mytheme = THEME_mytheme
    menu_mytheme.title_offset = (400, 70)
    menu_mytheme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=screen.get_height(),
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=menu_mytheme,
        title='Main menu',
        width=screen.get_width()
    )

    main_menu.add.button('Play',  level_select_menu)
    main_menu.add.button('Options', options_menu)
    main_menu.add.button('Scoreboard')
    main_menu.add.button('Change Username', pygame_menu.events.BACK)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    user_save.try_load()

    for index, lvl in enumerate(levels.levels.values()):
        level_select_menu.add.button(
            lvl.lvl_name, new_game, screen, levels.get_level(index), user_save)

        if index >= len(user_save.lvl_info):
            break
    # -------------------------------------------------------------------------
    # Create menus: Start
    # -------------------------------------------------------------------------
    start_mytheme = THEME_mytheme
    start_mytheme.title_offset = (150, 70)
    start_mytheme.widget_font_size = 30

    start = pygame_menu.Menu(
        height=screen.get_height(),
        onclose=pygame_menu.events.EXIT,  # User presses ESC button
        theme=start_mytheme,
        title='Marvin The Galaxy Typer',
        width=screen.get_width()
    )

    start.add.text_input('Username: ')
    start.add.button('OK', main_menu)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------

    if start_screen == "start":
        starting_menu = start
    elif start_screen == "main_menu":
        starting_menu = main_menu
    elif start_screen == "level_select":
        starting_menu = level_select_menu

    while True:

        # Tick
        clock.tick(FPS)

        # Main menu
        starting_menu.mainloop(surface, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()
