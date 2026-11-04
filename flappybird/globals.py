import os


class globals:
    # Bilder relativ zum Paket, damit das Spiel aus jedem Ordner startet
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "assets")

    FPS = 30
    SUB_IMAGE_SIZE = 16
    TILES_SIZE = 64

    ## WORLD GLOBALS ##
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    GRAVITY = 1                 # Pixels / FPS
    BIRD_SPEED = 4              # Pixels / FPS
    BIRD_FLAP_STRENGTH = -15    # Pixels / FPS

