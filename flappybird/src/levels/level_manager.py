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

    def check_result(self, dont_check_lost: bool = False):
        if self.check_done():
            self.current_level.reset_hooks()
            self._flappy_bird.completed = True
            print("✅ Level bestanden! Du kannst das Spiel beenden")
        else:
            if dont_check_lost:
                self.current_level.reset_hooks()
                self._flappy_bird.lost = True
                print("❌ Level nicht bestanden! Du kannst das Spiel beenden")

    def _run_student_solution(self):
        run_mode = self.current_level.run_mode
        run_interval_seconds = self.current_level.run_interval_seconds
        def __run_student_solution(self, run_mode: RunMode, interval_seconds: float):
            # ausgewählten modus ausführen
            try:
                # raise AttributeError("AttributeError")
                if run_mode == RunMode.Once:
                    # einmal ausführen und und kucken ob Lösung stimmt
                    self._student_code.solution()
                    self.check_result()
                elif run_mode == RunMode.Forever:
                    # wiederholen bis es stimmt oder exit
                    while self.game_running and not self.check_done():
                        self._student_code.solution()
                        time.sleep(interval_seconds)
                    if self.check_done():
                        self.check_result(dont_check_lost=True)
                        # hier gibt es kein "nicht bestanden" weil endlos
                elif run_mode == RunMode.Duration:
                    # wiederholen für eine bestimmte (gesetzte) Zeit
                    end_time = time.time() + self.current_level.run_duration
                    while self.game_running and time.time() < end_time and not self.check_done():
                        self._student_code.solution()
                        time.sleep(interval_seconds)
                    self.check_result()
                else:
                    self._student_code.solution()
            except Exception as e:
                self.game_stop()
                self.current_level.reset_hooks()
                raise e

        threading.Thread(target=__run_student_solution, args=(self, run_mode, run_interval_seconds), daemon=True).start()

    def _check_student_solution(self):
        def __check_student_solution(level_manager):
            # wartet bis abgeschlossen oder verloren
            while level_manager.game_running and not (level_manager.check_done() or level_manager._flappy_bird.lost):
                time.sleep(0.2)
            # danach Hooks wiederherstellen
            level_manager.reset()
            # dann warten bis Fenster geschlossen wird
            while level_manager.game_running:
                time.sleep(0.5)

        threading.Thread(target=__check_student_solution, args=(self,), daemon=True).start()

    def check_done(self) -> bool:
        return self.current_level and self.current_level.done and not self._flappy_bird.lost

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