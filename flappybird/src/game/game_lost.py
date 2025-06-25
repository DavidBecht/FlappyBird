import pygame
from flappybird.globals import globals as g

class GameLost:
    _image_path = "src/assets/game_lost.png"
    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        # load flappy bird images
        image = pygame.image.load(self._image_path).convert_alpha()
        self._image = pygame.transform.scale(image, (g.TILES_SIZE * 4, g.TILES_SIZE * 4))

    def draw(self):
        self._screen.blit(self._image, (g.SCREEN_WIDTH / 2 - g.TILES_SIZE * 2, g.SCREEN_HEIGHT - g.TILES_SIZE * 4 - 10))
