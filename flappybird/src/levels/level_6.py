from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase
from flappybird.globals import globals as g


class Level6(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)

    def validate(self, text: str) -> bool:
        from flappybird.game import bird

        if not text.strip():
            self.set_error("Es wird eine Ausgabe erwartet.")
            return False

        expected = "zu tief" if bird.position_y > g.SCREEN_HEIGHT / 2 else "zu hoch"
        normalized = " ".join(text.split()).lower()
        if normalized == expected:
            return True

        self.set_error(f"Erwartet wird '{expected}'.")
        return False
