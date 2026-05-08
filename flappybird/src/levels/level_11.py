import pygame.rect

from flappybird.src.game.game import FlappyBird
from flappybird.src.game.pipes import Pipe
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level11(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Duration
        self.run_duration = 8
        self.run_interval_seconds = 1 / g.FPS
        self.game._handle_pipes = True
        self.game._handle_collisions = True
        self.game._player._idle = True

        # ------------------ SINGLE PIPE ------------------
        start_x = g.SCREEN_WIDTH + 50

        x = start_x
        pipe = Pipe(
            screen=self.game._screen,
            pipe_body=self.game._pipes._pipe_body,
            pipe_head_up=self.game._pipes._pipe_head_up,
            pipe_head_down=self.game._pipes._pipe_head_down,
            spacing=0,
            height=1000,
            draw_hitboxes=self.game._pipes._draw_hitboxes
        )
        pipe._x_position = x
        pipe._rect_up.x = x
        pipe._rect_down.x = x
        # self.game._pipes._pipes.append(pipe)
        self.game._pipes.add_only_single_pipe(pipe)
        # ---------------------------------------------------


    def validate(self, text: str) -> bool:
        # LEVEL BEI DEM MAN auf eine pipes zugeht und man es stoppen muss (mit sensor checken)
        # ob es davor ist, man darf nicht in die wand gehen!
        from flappybird.game import bird

        if not text:
            self.set_error("Gib 'stopped' aus, wenn der Vogel stoppt.")
            return False

        # Grenzwert ist < 100, konsistent mit Aufgabenstellung in level_11.md.
        if bird.sensor_distances["right"] >= 100:
            self.set_error("Der Vogel soll erst bei Abstand < 100 Pixel stoppen.")
            return False

        if "stopped" not in text.lower():
            self.set_error("Die Ausgabe muss 'stopped' enthalten.")
            return False

        if not bird.is_stopped:
            self.set_error("Es wurde nicht gestoppt. Verwende bird.stop().")
            return False

        return True
