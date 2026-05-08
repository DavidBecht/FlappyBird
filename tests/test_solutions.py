import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import builtins
import argparse
import io
import contextlib
import importlib.util
import re

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

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;]*m")

# Global debug flag
DEBUG_MODE = False


def get_level_test_kwargs(level_number):
    """Return the mocked test inputs required to evaluate a specific level."""
    if level_number == 2:
        return {"input_side_effect": ["David"]}
    if level_number == 3:
        return {"input_side_effect": ["10"]}
    if level_number == 4:
        def bird_setup(mock_player):
            mock_player.position_y = 100
            mock_player.speed_abs = 10

        return {"bird_setup": bird_setup}
    if level_number == 5:
        def bird_setup(mock_player):
            mock_player.position_y = 100.5
            mock_player.speed_abs = 10.123
            mock_player.angle = 45.0

        return {"bird_setup": bird_setup}
    if level_number == 6:
        def bird_setup(mock_player):
            mock_player.position_y = 1000

        return {"bird_setup": bird_setup}
    if level_number == 8:
        def state1(player):
            player.distance = 100

        def state2(player):
            player.distance = 500

        return {"bird_states": [state1, state2]}
    if level_number in {9, 10}:
        def bird_setup(mock_player):
            mock_player.time_alive = 11

        return {"bird_setup": bird_setup}
    if level_number == 11:
        def bird_setup(mock_player):
            mock_player.sensor_distances = {"right": 99}
            mock_player.is_stopped = False

            def stop():
                mock_player.is_stopped = True

            mock_player.stop.side_effect = stop

        return {"bird_setup": bird_setup}
    if level_number == 14:
        def bird_setup(mock_player):
            mock_player.time_alive = 21

        return {"bird_setup": bird_setup}
    return {}


def sanitize_summary_message(message):
    """Strip ANSI codes and escape markdown-breaking characters for CI summaries."""
    cleaned_message = ANSI_ESCAPE_PATTERN.sub("", message)
    cleaned_message = cleaned_message.replace("\r", " ").replace("\n", " ").strip()
    return cleaned_message.replace("`", "\\`").replace("|", "\\|")

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
            # Print the assertion message nicely
            msg = str(err[1])
            if msg:
                for line in msg.split('\n'):
                    self.stream.writeln(f"    {line}")
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

    def get_solution_from_md(self, level_number):
        md_path = os.path.abspath(os.path.join(ROOT_DIR, 'angaben', f'level_{level_number}.md'))
        if not os.path.exists(md_path):
            self.fail(f"Markdown file for level {level_number} not found at {md_path}")
        
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find the solution block
        start_marker = ":::solution"
        end_marker = ":::"
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            self.fail(f"No solution block found in {md_path}")
            
        # Find the end of the solution block
        # We search from start_idx + len(start_marker)
        end_idx = content.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1:
             self.fail(f"No end marker for solution block found in {md_path}")
             
        solution_block = content[start_idx + len(start_marker):end_idx]
        
        # Extract python code block
        code_start_marker = "```python"
        code_end_marker = "```"
        
        code_start = solution_block.find(code_start_marker)
        if code_start == -1:
             # Try without python specifier
             code_start_marker = "```"
             code_start = solution_block.find(code_start_marker)
        
        if code_start == -1:
            self.fail(f"No code block found in solution of {md_path}")
            
        code_end = solution_block.find(code_end_marker, code_start + len(code_start_marker))
        if code_end == -1:
            self.fail(f"No end of code block found in solution of {md_path}")
            
        code = solution_block[code_start + len(code_start_marker):code_end].strip()
        
        # Create a function from the code
        # We need to exec the code in a local scope and extract the 'solution' function
        # We use the same dictionary for globals and locals so that imports at the top level
        # are available to the solution function.
        scope = {}
        try:
            exec(code, scope)
        except Exception as e:
            self.fail(f"Failed to parse solution code for level {level_number}: {e}")
            
        if 'solution' not in scope:
            self.fail(f"No 'solution' function defined in solution code for level {level_number}")
            
        print("\033[94m[MD]\033[0m ", end='', flush=True)
        return scope['solution']

    def get_solution_from_student_file(self, level_number, student_dir="student_solutions"):
        solution_path = os.path.abspath(os.path.join(ROOT_DIR, student_dir, f"level_{level_number}.py"))
        if not os.path.exists(solution_path):
            self.fail(f"Student solution for level {level_number} not found at {solution_path}")

        module_name = f"_student_level_{level_number}"
        spec = importlib.util.spec_from_file_location(module_name, solution_path)
        if spec is None or spec.loader is None:
            self.fail(f"Student solution for level {level_number} could not be loaded from {solution_path}")

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            self.fail(f"Student solution for level {level_number} could not be imported: {exc}")

        declared_level = getattr(module, "LEVEL", None)
        if declared_level is not None and declared_level != level_number:
            self.fail(
                f"Student solution file {solution_path} declares LEVEL = {declared_level}, expected {level_number}"
            )

        solution = getattr(module, "solution", None)
        if not callable(solution):
            self.fail(f"Student solution for level {level_number} must define a callable solution()")

        print("\033[96m[FILE]\033[0m ", end='', flush=True)
        return solution

    def run_level(
        self,
        level_number,
        solution_func=None,
        input_side_effect=None,
        bird_states=None,
        bird_setup=None,
        use_student_file=False,
        student_dir="student_solutions",
    ):
        # If solution_func is not provided, try to load it from MD
        if solution_func is None:
            if use_student_file:
                solution_func = self.get_solution_from_student_file(level_number, student_dir=student_dir)
            else:
                solution_func = self.get_solution_from_md(level_number)
        else:
            print(f"\033[93m[CODE]\033[0m ", end='', flush=True)

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
                captured_output = ""
                if not DEBUG_MODE:
                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        self._run_execution_loop(manager, solution_func, bird_states, mock_player)
                    captured_output = f.getvalue()
                else:
                    self._run_execution_loop(manager, solution_func, bird_states, mock_player)
                
                # Check if level is done
                if not manager.check_done():
                    msg = f"\n\033[91m[FAILED]\033[0m Level {level_number} not completed successfully."
                    reason = getattr(manager.current_level, "last_error", "")
                    if reason:
                        msg += f"\n\n\033[93mReason:\033[0m {reason}"
                    if captured_output:
                        msg += f"\n\n\033[93mCaptured Output:\033[0m\n{'-'*20}\n{captured_output}{'-'*20}"
                    self.fail(msg)
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
        self.run_level(1)

    def test_level_2(self):
        self.run_level(2, **get_level_test_kwargs(2))

    def test_level_3(self):
        self.run_level(3, **get_level_test_kwargs(3))

    def test_level_4(self):
        self.run_level(4, **get_level_test_kwargs(4))

    def test_level_5(self):
        self.run_level(5, **get_level_test_kwargs(5))

    def test_level_6(self):
        self.run_level(6, **get_level_test_kwargs(6))

    def test_level_7(self):
        self.run_level(7)

    def test_level_8(self):
        self.run_level(8, **get_level_test_kwargs(8))

    def test_level_9(self):
        self.run_level(9, **get_level_test_kwargs(9))

    def test_level_10(self):
        self.run_level(10, **get_level_test_kwargs(10))

    def test_level_11(self):
        self.run_level(11, **get_level_test_kwargs(11))

    def test_level_12(self):
        self.run_level(12)

    def test_level_13(self):
        self.run_level(13)

    def test_level_14(self):
        self.run_level(14, **get_level_test_kwargs(14))


def run_student_level_checks(student_dir="student_solutions", levels=range(1, 15)):
    """Run all available student level files and return a non-zero exit code on failures."""
    passed_levels = []
    failed_levels = []
    missing_levels = []

    for level_number in levels:
        solution_path = os.path.abspath(os.path.join(ROOT_DIR, student_dir, f"level_{level_number}.py"))
        if not os.path.exists(solution_path):
            missing_levels.append(level_number)
            continue

        checker = TestSolutions()
        checker.setUp()
        try:
            checker.run_level(
                level_number,
                use_student_file=True,
                student_dir=student_dir,
                **get_level_test_kwargs(level_number),
            )
        except Exception as exc:
            failed_levels.append((level_number, str(exc).strip() or repr(exc)))
        else:
            passed_levels.append(level_number)
        finally:
            checker.tearDown()

    summary_lines = [
        "# Level-Check Zusammenfassung",
        "",
        f"✅ Geschafft: {', '.join(map(str, passed_levels)) if passed_levels else '-'}",
        f"❌ Nicht geschafft: {', '.join(str(level) for level, _ in failed_levels) if failed_levels else '-'}",
        f"⏳ Noch keine Datei: {', '.join(map(str, missing_levels)) if missing_levels else '-'}",
    ]

    if failed_levels:
        summary_lines.extend(["", "## Fehlerdetails", ""])
        for level_number, message in failed_levels:
            summary_lines.append(f"- Level {level_number}: {sanitize_summary_message(message)}")

    summary_text = "\n".join(summary_lines)
    print()
    print(summary_text)

    github_summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary_path:
        with open(github_summary_path, "a", encoding="utf-8") as summary_file:
            summary_file.write("\n")
            summary_file.write(summary_text)
            summary_file.write("\n")

    return 1 if failed_levels else 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--student-files', action='store_true', help='Check split student solution files')
    parser.add_argument('--student-files-dir', default='student_solutions', help='Directory with level_*.py files')
    args, unknown = parser.parse_known_args()
    
    DEBUG_MODE = args.debug

    if args.student_files:
        sys.exit(run_student_level_checks(student_dir=args.student_files_dir))

    # Remove arguments so unittest doesn't complain
    sys.argv = [sys.argv[0]] + unknown

    unittest.main(verbosity=2)

    # run with python tests/test_solutions.py --debug
