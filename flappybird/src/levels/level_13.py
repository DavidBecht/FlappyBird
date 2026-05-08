import re
from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase


class Level13(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)

    def validate(self, text: str) -> bool:
        return bool(re.search(r'\b5050\b', text))
