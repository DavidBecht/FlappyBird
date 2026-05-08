from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g


class Level14(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Duration
        self.run_duration = 22
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = False
        self.game._handle_collisions = True
        self.game._handle_pipes = True
        self.game._pipes._spacing = 250
        self.game._pipes._height = (g.SCREEN_HEIGHT - self.game._pipes._spacing) // 2
        self.game._pipes._spawn_time = 2.0

    def validate(self, text: str) -> bool:
        from flappybird.game import bird
        return bird.time_alive > 20
