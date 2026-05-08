import re

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level9(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Forever
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = False
        self.game._handle_collisions = True
        self.game._handle_pipes = False

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

        self.set_error("FlappyBird muss mindestens 10 Sekunden überleben (kleine Toleranz erlaubt).")
        return False
