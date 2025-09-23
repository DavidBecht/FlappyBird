from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode
from flappybird.globals import globals as g
class Level10(LevelBase):
    def __init__(self, game: FlappyBird):
        super().__init__(game)
        self.run_mode = RunMode.Forever
        self.run_interval_seconds = 1 / g.FPS
        self.game._player._idle = False
        self.game._handle_collisions = True
        self.game._handle_pipes = True
        self.game._pipes._spacing = 300
        self.game._pipes._height = (g.SCREEN_HEIGHT - self.game._pipes._spacing) // 2
        self.game._pipes._spawn_time = 1.5
    def validate(self, text: str) -> bool:
        from flappybird.game import bird
        if text:
            splits = text.split(" ")
            if len(splits) == 3:
                try:
                    alive_time = float(splits[1])
                    if text.startswith("Alive:") and alive_time > 10 and bird.time_alive > 10:
                        return True
                except:
                    pass
        return False