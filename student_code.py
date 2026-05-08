from functools import lru_cache
import importlib

LEVEL = 11


@lru_cache(maxsize=None)
def _load_student_module(level):
    module_name = f"student_solutions.level_{level}"
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if exc.name == module_name:
            raise ModuleNotFoundError(f"Missing student solution file for level {level}: {module_name}.py") from exc
        raise
    except ImportError as exc:
        raise ImportError(f"Could not import {module_name}: {exc}") from exc


def solution():
    module = _load_student_module(LEVEL)
    student_solution = getattr(module, "solution", None)
    if not callable(student_solution):
        raise AttributeError(f"student_solutions.level_{LEVEL} must define solution()")
    return student_solution()
