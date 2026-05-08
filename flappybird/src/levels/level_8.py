import re

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level8(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Forever
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = True
        self._first_true = False

    def validate(self, text: str) -> bool:
        if not text:
            self.set_error("Es wurde nichts ausgegeben.")
            return False
        from flappybird.game import bird
        normalized = " ".join(text.split())
        if bird.distance < 500:
            match = re.fullmatch(r"erst\s+([-+]?\d*\.?\d+)\s+pixel", normalized, re.IGNORECASE)
            if not match:
                self._first_true = False
                self.set_error("Bei Distanz < 500 wird 'Erst <Distanz> Pixel' erwartet.")
                return False
            distance = float(match.group(1))
            if distance <= bird.distance:
                self._first_true = True
            else:
                self._first_true = False
                self.set_error("Der ausgegebene Distanzwert ist größer als die aktuelle Distanz.")
                return False
        elif bird.distance >= 500:
            if normalized.lower() == "juhu" and self._first_true:
                return True
            if not self._first_true:
                self.set_error("Vor 'Juhu' muss zuerst die Distanz-Ausgabe bei < 500 erfolgen.")
            else:
                self.set_error("Bei Distanz >= 500 wird exakt 'Juhu' erwartet.")
            self._first_true = False
        return False
