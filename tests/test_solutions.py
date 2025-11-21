import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import builtins
import argparse
import io
import contextlib

# Mock pygame before importing flappybird
sys.modules["pygame"] = MagicMock()
sys.modules["pygame.rect"] = MagicMock()
sys.modules["pygame.event"] = MagicMock()
sys.modules["pygame.image"] = MagicMock()
sys.modules["pygame.display"] = MagicMock()
sys.modules["pygame.time"] = MagicMock()
sys.modules["pygame.transform"] = MagicMock()

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Global debug flag
DEBUG_MODE = False

class ColoredTextTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        # Force verbosity to 2 (showAll) to get the full output format
        super().__init__(stream, descriptions, 2)

    def addSuccess(self, test):
        # Call grandparent to avoid printing 'ok'
        unittest.TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.write("\033[92mOK\033[0m")
            self.stream.writeln()
        elif self.dots:
            self.stream.write("\033[92m.\033[0m")
            self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.write("\033[91mFAIL\033[0m")
            self.stream.writeln()
        elif self.dots:
            self.stream.write("\033[91mF\033[0m")
            self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.write("\033[91mERROR\033[0m")
            self.stream.writeln()
        elif self.dots:
            self.stream.write("\033[91mE\033[0m")
            self.stream.flush()
            
    def startTest(self, test):
        super().startTest(test)

# Monkey patch unittest.TextTestRunner to use our result class by default
unittest.TextTestRunner.resultclass = ColoredTextTestResult

class TestSolutions(unittest.TestCase):
    
    def setUp(self):
        self.original_modules = sys.modules.copy()
        # If running in a tool like PyCharm (not __main__), manually print start
        if __name__ != '__main__':
            print(f"{self.id()} ... ", end='', flush=True)
        
    def tearDown(self):
        # If running in a tool like PyCharm, manually print result
        if __name__ != '__main__':
            # Check result
            # This logic works for Python 3.4+
            if hasattr(self, '_outcome'):
                # Check if there are any errors in the outcome
                # self._outcome.errors is a list of (test_case, exc_info)
                # If exc_info is not None, it's a failure/error
                failed = False
                if hasattr(self._outcome, 'errors'):
                    for _, exc_info in self._outcome.errors:
                        if exc_info:
                            failed = True
                            break
                
                # Also check result if available (some runners set it)
                if not failed and hasattr(self._outcome, 'result'):
                     # This is less reliable as result object varies
                     pass

                if failed:
                     print("\033[91mFAIL/ERROR\033[0m")
                else:
                     print("\033[92mOK\033[0m")

        # We don't restore sys.modules fully because it breaks things, 
        # but we should be careful about side effects.
        pass

    def run_level(self, level_number, solution_func, input_side_effect=None, bird_states=None, bird_setup=None):
        # Mock student_code
        student_code_mock = MagicMock()
        student_code_mock.LEVEL = level_number
        student_code_mock.solution = solution_func
        
        with patch.dict(sys.modules, {"student_code": student_code_mock}):
            # Re-import LevelManager to pick up the new student_code
            if "flappybird.src.levels.level_manager" in sys.modules:
                del sys.modules["flappybird.src.levels.level_manager"]
            
            from flappybird.src.levels.level_manager import LevelManager
            import flappybird.src.levels.level_manager_instance as lmi
            
            # Mock FlappyBird
            with patch("flappybird.src.levels.level_manager.FlappyBird") as MockFlappyBird:
                mock_game = MockFlappyBird.return_value
                mock_game.running = True
                mock_game.lost = False
                mock_game.completed = False
                
                # Mock player
                mock_player = MagicMock()
                mock_game._player = mock_player
                mock_player.print = MagicMock()
                
                # Default bird values
                mock_player.position_y = 0
                mock_player.speed_abs = 0
                mock_player.angle = 0
                mock_player.distance = 0
                mock_player.time_alive = 0
                mock_player.sensor_distances = {"up": 999, "down": 999, "left": 999, "right": 999}
                mock_player.is_stopped = False
                
                if bird_setup:
                    bird_setup(mock_player)

                # Setup input handling
                if input_side_effect:
                    input_iter = iter(input_side_effect)
                    def start_input_side_effect(callback, update_callback=None):
                        try:
                            val = next(input_iter)
                        except StopIteration:
                            val = ""
                        callback(val)
                    
                    mock_player._speech_bubble.start_input.side_effect = start_input_side_effect
                else:
                     def start_input_side_effect(callback, update_callback=None):
                         callback("")
                     mock_player._speech_bubble.start_input.side_effect = start_input_side_effect
                
                # Initialize LevelManager
                manager = LevelManager()
                lmi.level_manager = manager
                manager.load_level()
                
                # Suppress output if not debug
                if not DEBUG_MODE:
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        self._run_execution_loop(manager, solution_func, bird_states, mock_player)
                else:
                    self._run_execution_loop(manager, solution_func, bird_states, mock_player)
                
                # Check if level is done
                if not manager.check_done():
                    self.fail(f"Level {level_number} not completed successfully.")

    def _run_execution_loop(self, manager, solution_func, bird_states, mock_player):
        if bird_states:
            for state_setup in bird_states:
                state_setup(mock_player)
                self._execute_solution(manager, solution_func)
                if manager.check_done():
                    break
        else:
            self._execute_solution(manager, solution_func)

    def _execute_solution(self, manager, solution_func):
        manager.current_level.apply_hooks()
        try:
            solution_func()
        finally:
            manager.current_level.reset_hooks()

    def test_level_1(self):
        def solution():
            # ENTER SOLUTION HERE
            print("Hi, World!")
            pass
        
        self.run_level(1, solution)

    def test_level_2(self):
        def solution():
            # ENTER SOLUTION HERE
            print("Wie heißt du?")
            name = input()
            print(f"Hi, {name}!")
            pass
        
        self.run_level(2, solution, input_side_effect=["David"])

    def test_level_3(self):
        def solution():
            # ENTER SOLUTION HERE
            print("Wie alt bist du?")
            age = int(input())
            print(f"Hi, ich bin immer\n5 Jahre älter als\ndu also {age}+5={age + 5}")
            pass
        
        self.run_level(3, solution, input_side_effect=["10"])

    def test_level_4(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            print(f"Ich bin bird!\nPosY.={bird.position_y}\nGeschwAbs.={bird.speed_abs}")
            pass
        
        def bird_setup(mock_player):
            mock_player.position_y = 100
            mock_player.speed_abs = 10
            
        self.run_level(4, solution, bird_setup=bird_setup)

    def test_level_5(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            print(f"Ich bin bird!\n" \
                  f"PosY.={bird.position_y: 12.2f} Pixel\n" \
                  f"GeschwAbs.={bird.speed_abs:7.2f} Pixel/s\n" \
                  f"Winkel.={bird.angle:9.1f} Grad")
            pass
        
        def bird_setup(mock_player):
            mock_player.position_y = 100.5
            mock_player.speed_abs = 10.123
            mock_player.angle = 45.0
            
        self.run_level(5, solution, bird_setup=bird_setup)

    def test_level_8(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            if bird.distance < 500:
                print(f"Erst {bird.distance} Pixel")
            else:
                print("Juhu")
            pass
        
        def state1(p): p.distance = 100
        def state2(p): p.distance = 500
        
        self.run_level(8, solution, bird_states=[state1, state2])

    def test_level_9(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            print(f"Alive: {bird.time_alive} s")
            pass
        
        def bird_setup(mock_player):
            mock_player.time_alive = 11
            
        self.run_level(9, solution, bird_setup=bird_setup)

    def test_level_10(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            print(f"Alive: {bird.time_alive} s")
            pass
        
        def bird_setup(mock_player):
            mock_player.time_alive = 11
            
        self.run_level(10, solution, bird_setup=bird_setup)

    def test_level_11(self):
        def solution():
            # ENTER SOLUTION HERE
            from flappybird.game import bird
            if bird.sensor_distances["right"] < 120:
                bird.stop()
                print("stopped")
            pass
        
        def bird_setup(mock_player):
            mock_player.sensor_distances = {"right": 100}
            mock_player.is_stopped = False
            def stop():
                mock_player.is_stopped = True
            mock_player.stop.side_effect = stop
            
        self.run_level(11, solution, bird_setup=bird_setup)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args, unknown = parser.parse_known_args()
    
    DEBUG_MODE = args.debug
    
    # Remove arguments so unittest doesn't complain
    sys.argv = [sys.argv[0]] + unknown
    
    unittest.main(verbosity=2)

    # run with python tests/test_solutions.py --debug*
    # *optional
