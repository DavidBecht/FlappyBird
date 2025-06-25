import random
import pygame
from flappybird.globals import globals as g

class Pipe:
    def __init__(self, screen: pygame.Surface, pipe_body: pygame.Surface,
                 pipe_head_up: pygame.Surface, pipe_head_down: pygame.Surface,
                 draw_hitboxes: bool = False):
        self._screen = screen
        self._draw_hitboxes = draw_hitboxes
        self._x_position = g.SCREEN_WIDTH
        self._pipe_body = pipe_body
        self._pipe_head_up = pipe_head_up
        self._pipe_head_down = pipe_head_down
        self._spaceing = 300
        min_height = int(g.SCREEN_HEIGHT / 100 * 10)
        max_height = int(g.SCREEN_HEIGHT / 100 * 50)
        self._height = random.randint(min_height, max_height)
        self._rect_up = pygame.Rect(self._x_position, 0, self._pipe_body.get_width(), self._height)
        self._rect_down = pygame.Rect(self._x_position, self._height + self._spaceing, self._pipe_body.get_width(), g.SCREEN_HEIGHT - (self._height + self._spaceing))

    def move(self, speed_px = 1) -> None:
        self._x_position -= speed_px
        self._rect_up.x = self._x_position
        self._rect_down.x = self._x_position

    def is_outside_screen(self) -> bool:
        if self._x_position + self._pipe_body.get_width() < 0:
            return True
        return False

    def is_over_half_screen(self) -> bool:
        if self._x_position + self._pipe_body.get_width() < g.SCREEN_WIDTH / 2:
            return True
        return False

    def is_colliding(self, player_rect: pygame.Rect) -> bool:
        return self._rect_up.colliderect(player_rect) or self._rect_down.colliderect(player_rect)

    def draw(self) -> None:
        # draw upper pipe bodies
        for i in range(0, self._height - self._pipe_head_down.get_height(), g.TILES_SIZE):
            self._screen.blit(self._pipe_body, (self._x_position, i))
        # draw pipe head
        self._screen.blit(self._pipe_head_down, (self._x_position, self._height - self._pipe_head_down.get_height()))
        # add spacing between pipes
        lower_height = self._height + self._spaceing
        self._screen.blit(self._pipe_head_up, (self._x_position, lower_height))
        lower_height += g.TILES_SIZE
        # draw lower pipe bodies
        for i in range(lower_height, g.SCREEN_HEIGHT, g.TILES_SIZE):
            self._screen.blit(self._pipe_body, (self._x_position, i))
        if self._draw_hitboxes:
            pygame.draw.rect(self._screen, "red", self._rect_up, 1)
            pygame.draw.rect(self._screen, "red", self._rect_down, 1)


class Pipes:
    _image_pipe_path = "src/assets/Tiles/Style 1/PipeStyle1.png"
    def __init__(self, screen: pygame.Surface, draw_hitboxes: bool = False):
        self._screen = screen
        self._draw_hitboxes = draw_hitboxes
        self._pipes: list[Pipe] = []
        self._last_timestamp = None
        # load pipes
        pipes_img = pygame.image.load(self._image_pipe_path).convert_alpha()

        img = pipes_img.subsurface((0, 0, g.SUB_IMAGE_SIZE * 2, g.SUB_IMAGE_SIZE * 2))
        self._pipe_head_up = pygame.transform.scale(img, (g.TILES_SIZE*2, g.TILES_SIZE))
        img = pipes_img.subsurface((0, g.SUB_IMAGE_SIZE * 2, g.SUB_IMAGE_SIZE * 2, g.SUB_IMAGE_SIZE))
        self._pipe_body = pygame.transform.scale(img, (g.TILES_SIZE * 2, g.TILES_SIZE))
        img = pipes_img.subsurface((0, g.SUB_IMAGE_SIZE * 3, g.SUB_IMAGE_SIZE * 2, g.SUB_IMAGE_SIZE * 2))
        self._pipe_head_down = pygame.transform.scale(img, (g.TILES_SIZE * 2, g.TILES_SIZE))

    def is_colliding(self, player: pygame.Rect) -> bool:
        for pipe in self._pipes:
            if pipe.is_colliding(player):
                return True
        return False

    def draw(self):
        if len(self._pipes) == 0 or \
                (len(self._pipes) == 1 and self._pipes[0].is_over_half_screen()):
            self._pipes.append(Pipe(screen=self._screen,
                                    pipe_body=self._pipe_body,
                                    pipe_head_up=self._pipe_head_up,
                                    pipe_head_down=self._pipe_head_down,
                                    draw_hitboxes=self._draw_hitboxes))
        for pipe in reversed(self._pipes):
            pipe.move(g.BIRD_SPEED)
            if pipe.is_outside_screen():
                self._pipes.remove(pipe)
                continue
            pipe.draw()




