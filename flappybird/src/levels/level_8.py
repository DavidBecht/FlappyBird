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
            return False
        from flappybird.game import bird
        if bird.distance < 500:
            text_splitted = text.split(" ")
            if len(text_splitted) != 3:
                self._first_true = False
                return False
            try:
                distance = float(text_splitted[1])
            except:
                self._first_true = False
                return False
            if distance <= bird.distance and text_splitted[0] == "Erst" and text_splitted[2] == "Pixel":
                self._first_true = True
        elif bird.distance >= 500 and text == "Juhu" and self._first_true:
            return True
        else:
            self._first_true = False
        return False