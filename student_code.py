from functools import lru_cache
import importlib

LEVEL = 11


@lru_cache(maxsize=None)
def _load_student_module(level):
    return importlib.import_module(f"student_solutions.level_{level}")


def solution():
    module = _load_student_module(LEVEL)
    student_solution = getattr(module, "solution", None)
    if not callable(student_solution):
        raise AttributeError(f"student_solutions.level_{LEVEL} must define solution()")
    return student_solution()
