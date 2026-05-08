import re

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level5(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Forever
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = True

    def validate(self, text: str) -> bool:
        from flappybird.game import bird

        if bird.speed_abs > 0:
            lines = [line.strip() for line in text.replace("\r", "").splitlines() if line.strip()]
            if len(lines) != 4:
                self.set_error("Erwartet werden vier Zeilen: Titel, PosY, GeschwAbs und Winkel.")
                return False

            if lines[0].lower() != "ich bin bird!":
                self.set_error("Die erste Zeile muss 'Ich bin bird!' lauten.")
                return False

            pos_match = re.fullmatch(r"posy\.\s*=\s*([-+]?\d*\.?\d+)\s*pixel", lines[1], re.IGNORECASE)
            speed_match = re.fullmatch(r"geschwabs\.\s*=\s*([-+]?\d*\.?\d+)\s*pixel/(?:s|sec)", lines[2], re.IGNORECASE)
            angle_match = re.fullmatch(r"winkel\.\s*=\s*([-+]?\d*\.?\d+)\s*grad", lines[3], re.IGNORECASE)

            if not pos_match or not speed_match or not angle_match:
                self.set_error("Eine Zeile ist nicht im erwarteten Format mit Einheit.")
                return False

            pos_value = float(pos_match.group(1))
            speed_value = float(speed_match.group(1))
            angle_value = float(angle_match.group(1))

            if abs(pos_value - bird.position_y) > 0.01:
                self.set_error("PosY ist nicht korrekt auf den Bird-Wert bezogen.")
                return False
            if abs(speed_value - bird.speed_abs) > 0.01:
                self.set_error("GeschwAbs ist nicht korrekt auf den Bird-Wert bezogen.")
                return False
            if abs(angle_value - bird.angle) > 0.1:
                self.set_error("Winkel ist nicht korrekt auf den Bird-Wert bezogen.")
                return False

            return True
        else:
            self.set_error("Warte auf Bewegung des Vogels und gib dann formatierte Werte aus.")
        return False
