import pygame

from flappybird.src.game.game_lost import GameLost
from flappybird.src.game.pipes import Pipes
from flappybird.src.game.world import World
from flappybird.src.player.level_completed import LevelCompleted
from flappybird.src.player.player import Player
from flappybird.globals import globals as g
class FlappyBird:
    def __init__(self, handle_collisions: bool = False, play_with_keyboard: bool = False, show_hitboxes:bool = False,
                 handle_pipes=False):
        self._handle_collisions = handle_collisions
        self._play_with_keyboard = play_with_keyboard

        pygame.init()
        self._screen = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))
        # init game clock
        self._clock = pygame.time.Clock()
        # init world
        self._world = World(self._screen)
        self._world.switch_world(1)
        # init pipes
        self._handle_pipes = handle_pipes
        self._pipes = Pipes(self._screen, show_hitboxes)

        # init player
        self._player = Player(self._screen, show_hitbox=show_hitboxes, pipes=self._pipes)
        # init level completed patch
        self._level_completed = LevelCompleted(self._screen)
        self._game_lost = GameLost(self._screen)

        # init gameloop variables
        self._running = True
        self._completed = False
        self._lost = False

    def get_obstacles(self) -> list[pygame.rect.Rect]:
        return self._pipes.get_rects() if self._handle_pipes else []

    def start(self):
        # init gameloop variables
        self._running = True

        while self._running:
            jump = False
            for event in pygame.event.get():
                self._player.handle_event(event)
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.KEYDOWN and self._play_with_keyboard:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                    elif event.key == pygame.K_SPACE:
                        jump = True
                elif event.type == pygame.MOUSEBUTTONDOWN and self._play_with_keyboard:
                    if pygame.mouse.get_pressed()[0] == 1:
                        jump = True
            self._screen.fill("white")
            self._world.draw()
            if self._handle_pipes:
                self._pipes.draw()
            if jump:
                self._player.jump()
            self._player.move()
            if self._completed and not self._lost:
                self._level_completed.draw()
            elif self._handle_collisions and not self._completed and not self._lost:
                # check if player collided with a pipe
                if self._handle_pipes:
                    self._lost = self._pipes.is_colliding(self._player.get_rect()) or \
                        not self._screen.get_rect().colliderect(self._player.get_rect())
                else:
                    self._lost = not self._screen.get_rect().colliderect(self._player.get_rect())
            elif self._handle_collisions and not self._completed and self._lost:
                self._game_lost.draw()
            elif not self._completed and self._lost:
                self._game_lost.draw()

            pygame.display.flip()

            self._clock.tick(g.FPS)
        pygame.quit()

    @property
    def running(self) -> bool:
        return self._running

    @property
    def lost(self) -> bool:
        return self._lost

    @lost.setter
    def lost(self, value: bool) -> None:
        self._lost = value

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool) -> None:
        self._completed = value

    @property
    def is_w_key_pressed(self) -> bool:
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[pygame.K_w]

    @property
    def is_s_key_pressed(self) -> bool:
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys[pygame.K_s]