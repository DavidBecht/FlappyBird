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
            solution = f"Ich bin bird!\nPosY.={bird.position_y}\nGeschwAbs.={bird.speed_abs}"
            if text.strip().lower() == solution.lower():
                return True
        return False