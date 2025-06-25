import pygame
from flappybird.globals import globals as g

class World:
    _image_path = "src/assets/Background/Background?.png"

    def __init__(self, screen: pygame.Surface):
        self._screen = screen
        self._x_pos = 0
        self._world_number = 0
        #  load background
        self._world_images: list[pygame.Surface] = []
        self._world_image_size = screen.get_height()
        for i in range(9):
            image = pygame.image.load(self._image_path.replace('?', str(i + 1))).convert_alpha()
            image = pygame.transform.scale(image, (self._world_image_size, self._world_image_size))
            self._world_images.append(image)


    def switch_world(self, number: int):
        self._world_number = number % 9
    def draw(self):
        width = self._world_image_size - self._x_pos
        image = self._world_images[self._world_number]
        first_image = image.subsurface((self._x_pos, 0, width, self._world_image_size))
        self._screen.blit(first_image, (0, 0))
        for i in range(width, self._screen.get_width(), self._world_image_size):
            self._screen.blit(image, (i, 0))
        self._x_pos = (self._x_pos + g.BIRD_SPEED) % self._screen.get_height()
