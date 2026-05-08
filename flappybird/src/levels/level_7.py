from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase


class Level7(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self._printed_numbers: list[int] = []

    def validate(self, text: str) -> bool:
        stripped = text.strip()
        if stripped.isdigit():
            self._printed_numbers.append(int(stripped))

        if self._printed_numbers == [1, 2, 3]:
            return True

        if len(self._printed_numbers) >= 3 and self._printed_numbers != [1, 2, 3]:
            self.set_error("Erwartet werden die Zahlen 1, 2, 3 jeweils in eigener Zeile.")
        elif self._printed_numbers:
            self.set_error("Es fehlen noch Zahlen. Erwartet ist die Folge 1, 2, 3.")
        else:
            self.set_error("Nutze eine Schleife und gib 1, 2, 3 aus.")
        return False
