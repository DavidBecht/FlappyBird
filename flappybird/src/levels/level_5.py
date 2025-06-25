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
            solution = f"Ich bin bird!\n" \
                f"PosY.={bird.position_y: 12.2f} Pixel\n" \
                f"GeschwAbs.={bird.speed_abs:7.2f} Pixel/s\n" \
                f"Winkel.={bird.angle:9.1f} Grad"
            if text.strip().lower() == solution.lower():
                return True
        return False