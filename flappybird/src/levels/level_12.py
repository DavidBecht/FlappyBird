from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase


class Level12(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self._printed_numbers: list[int] = []

    def validate(self, text: str) -> bool:
        stripped = text.strip()
        if stripped.isdigit():
            self._printed_numbers.append(int(stripped))
        return self._printed_numbers == list(range(1, 11))
