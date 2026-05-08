import re

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode

class Level4(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Forever
        self.run_interval_seconds = 0.2

    def validate(self, text: str) -> bool:
        from flappybird.game import bird

        if bird.speed_abs > 0:
            lines = [line.strip() for line in text.replace("\r", "").splitlines() if line.strip()]
            if len(lines) != 3:
                self.set_error("Erwartet werden drei Zeilen: Titel, PosY und GeschwAbs.")
                return False

            if lines[0].lower() != "ich bin bird!":
                self.set_error("Die erste Zeile muss 'Ich bin bird!' lauten.")
                return False

            pos_match = re.fullmatch(r"posy\.\s*=\s*([-+]?\d*\.?\d+)", lines[1], re.IGNORECASE)
            speed_match = re.fullmatch(r"geschwabs\.\s*=\s*([-+]?\d*\.?\d+)", lines[2], re.IGNORECASE)

            if not pos_match or not speed_match:
                self.set_error("PosY oder GeschwAbs sind nicht im erwarteten Format.")
                return False

            pos_value = float(pos_match.group(1))
            speed_value = float(speed_match.group(1))

            if abs(pos_value - bird.position_y) > 1e-6:
                self.set_error("PosY entspricht nicht dem aktuellen Bird-Wert.")
                return False
            if abs(speed_value - bird.speed_abs) > 1e-6:
                self.set_error("GeschwAbs entspricht nicht dem aktuellen Bird-Wert.")
                return False

            return True
        else:
            self.set_error("Warte auf Bewegung des Vogels und gib dann die Werte aus.")
        return False
