import re
from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase


class Level13(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)

    def validate(self, text: str) -> bool:
        normalized = " ".join(text.lower().split())
        if re.search(r"\bdie summe von 1 bis 100 ist 5050\b", normalized):
            return True
        if "5050" not in normalized:
            self.set_error("Die richtige Summe 5050 wurde nicht ausgegeben.")
        else:
            self.set_error("Erwartet wird der Satz: 'Die Summe von 1 bis 100 ist 5050'.")
        return False
