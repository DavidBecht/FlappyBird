import builtins
import threading

from enum import Enum

from flappybird.src.game.game import FlappyBird


# class syntax
class RunMode(Enum):
    Once = 1
    Forever = 2
    Duration = 3

class LevelBase:
    def __init__(self, game: FlappyBird):
        self.original_print = builtins.print
        self.original_input = builtins.input
        self.game = game
        self._done = False

        # Optional: Eingabepuffer für automatische Tests
        self.input_values = []

        # Ausführungsmodus: "once" oder "duration"
        self.run_mode = RunMode.Once
        self.run_duration = 1.0  # in Sekunden
        self.run_interval_seconds = 0.1  # wie oft solution() pro Sekunde bei "duration"

    def check_print(self, *args, **kwargs):
        text = " ".join(str(arg) for arg in args)
        self.game._player.print(text)
        self.original_print(*args, **kwargs)
        # try:
        if self.validate(text):
            self._done = True
        # except Exception as e:
        #     traceback.print_exc()
        #     raise e
        # finally:
        #     self.reset_hooks()


    def check_input(self, prompt=""):
        # print(prompt, end="")
        # value = self.original_input()
        # self.input_values.append(value)
        # self.game._player.print(value)
        #
        # return value
        print(prompt, end="")

        result_holder = {"value": None}
        done = threading.Event()

        def on_input_finished(text):
            result_holder["value"] = text
            done.set()

        def on_input_update(text):
            self.original_print(f"\r{prompt}{text}", end="", flush=True)

        self.game._player._speech_bubble.start_input(callback=on_input_finished, update_callback=on_input_update)

        # Warten, bis Eingabe abgeschlossen
        done.wait()
        print()
        self.input_values.append(result_holder["value"])
        return result_holder["value"]

    def apply_hooks(self):
        builtins.print = self.check_print
        builtins.input = self.check_input

    def reset_hooks(self):
        builtins.print = self.original_print
        builtins.input = self.original_input

    def validate(self, text: str) -> bool:
        raise NotImplementedError("Bitte überschreibe validate() in deinem Level.")

    @property
    def done(self) -> bool:
        if self.run_mode != RunMode.Once and not self._done :
            self._done = self.validate("")
        return self._done