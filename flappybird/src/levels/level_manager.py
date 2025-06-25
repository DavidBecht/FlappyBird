import importlib
import threading
import time

from flappybird.src.game.game import FlappyBird
from flappybird.src.levels.level_base import LevelBase, RunMode

class LevelManager:
    def __init__(self):
        import student_code
        self._student_code = student_code
        self._flappy_bird = FlappyBird(show_hitboxes=False)
        self.current_level = getattr(student_code, "LEVEL", None)
        if not self.current_level:
            raise AttributeError("LEVEL nicht definiert!")

    def load_level(self) -> None:
        try:
            module = importlib.import_module(f"flappybird.src.levels.level_{self.current_level}")
            level_class = getattr(module, f"Level{self.current_level}")
            self.current_level: LevelBase = level_class(self._flappy_bird)
            self.current_level.apply_hooks()
        except Exception as e:
            raise Exception(f"Fehler beim Laden von Level {self.current_level}: {e}")

    def start_game(self):
        self._run_student_solution()
        self._check_student_solution()
        self._flappy_bird.start()


    def _run_student_solution(self):
        run_mode = self.current_level.run_mode
        run_interval_seconds = self.current_level.run_interval_seconds

        def __check_done(self):
            if self.check_done():
                self.current_level.reset_hooks()
                self._flappy_bird.completed = True
                print("✅ Level bestanden! Du kannst das Spiel beenden")
                self.current_level.apply_hooks()
        def __run_student_solution(self, run_mode: RunMode, interval_seconds: float):
            # Schülerlösung in einem separaten Thread ausführen
            try:
                if run_mode == RunMode.Once:
                    self._student_code.solution()
                    __check_done(self)
                elif run_mode == RunMode.Forever:
                    while True:
                        self._student_code.solution()
                        __check_done(self)
                        time.sleep(interval_seconds)
            except Exception as e:
                self.game_stop()
                self.current_level.reset_hooks()
                raise e

        threading.Thread(target=__run_student_solution, args=(self, run_mode, run_interval_seconds), daemon=True).start()

    def _check_student_solution(self):
        def __check_student_solution(level_manager):
            # Warten bis Level abgeschlossen
            while not level_manager.check_done() and level_manager.game_running:
                time.sleep(0.5)

            level_manager.reset()

            while level_manager.game_running:
                time.sleep(0.5)

        threading.Thread(target=__check_student_solution, args=(self,), daemon=True).start()

    def check_done(self) -> bool:
        return self.current_level and self.current_level.done

    def reset(self):
        if self.current_level:
            self.current_level.reset_hooks()

    @property
    def game_running(self) -> bool:
        return self._flappy_bird.running

    @property
    def bird(self):
        if self._flappy_bird is None:
            raise RuntimeError("FlappyBird wurde noch nicht geladen. Bitte erst load_level() aufrufen.")
        return self._flappy_bird._player

    def game_stop(self):
        if self.game_running:
            self._flappy_bird._running = False