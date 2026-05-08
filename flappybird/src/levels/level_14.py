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
        self._uses_sensor = False
        self._uses_control = False

        try:
            import student_code
            solution = getattr(student_code, "solution", None)
            code_object = getattr(solution, "__code__", None)
            names = set(getattr(code_object, "co_names", ()))
            self._uses_sensor = "sensor_distances" in names
            self._uses_control = bool({"jump", "stop"} & names)
        except Exception:
            pass

    def validate(self, text: str) -> bool:
        from flappybird.game import bird
        if bird.time_alive <= 20:
            self.set_error("Der Vogel muss mindestens 20 Sekunden überleben.")
            return False
        if not self._uses_sensor:
            self.set_error("Nutze bird.sensor_distances für den Autopiloten.")
            return False
        if not self._uses_control:
            self.set_error("Steuere den Vogel aktiv, z. B. mit bird.jump().")
            return False
        return True
