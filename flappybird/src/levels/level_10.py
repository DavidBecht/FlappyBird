import re

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level10(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Duration
        self.run_duration = 12
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = False
        self.game._handle_collisions = True
        self.game._handle_pipes = True
        self.game._pipes._spacing = 300
        self.game._pipes._height = (g.SCREEN_HEIGHT - self.game._pipes._spacing) // 2
        self.game._pipes._spawn_time = 1.5

    def validate(self, text: str) -> bool:
        from flappybird.game import bird
        if not text:
            self.set_error("Es wird eine Alive-Ausgabe erwartet.")
            return False

        normalized = " ".join(text.split())
        match = re.fullmatch(r"alive:\s*([-+]?\d*\.?\d+)\s*(s|sec)", normalized, re.IGNORECASE)
        if not match:
            self.set_error("Erwartetes Format: 'Alive: <Sekunden> s'.")
            return False

        alive_time = float(match.group(1))
        if alive_time >= 9.8 and bird.time_alive >= 9.8:
            return True

        self.set_error("FlappyBird muss trotz Röhren mindestens 10 Sekunden überleben.")
        return False
