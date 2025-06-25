from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase

class Level3(LevelBase):

    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self._first_print = False

    def validate(self, text: str) -> bool:
        if text.lower().strip() == "wie alt bist du?":
            self._first_print = True
        if len(self.input_values) == 1:
            try:
                alter = int(self.input_values[0])
            except:
                pass
            solution = f'Hi, ich bin immer\n5 Jahre älter als\ndu also {alter}+5={alter + 5}'.lower()
            return text.lower().strip() == solution and self._first_print
        return False