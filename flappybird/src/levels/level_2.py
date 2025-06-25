from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase

class Level2(LevelBase):

    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self._first_print = False

    def validate(self, text: str) -> bool:
        if text.lower().strip() == "wie heißt du?":
            self._first_print = True
        if len(self.input_values) == 1:
            return text.lower().strip() == f"hi, {self.input_values[0].lower()}!" and self._first_print
        return False