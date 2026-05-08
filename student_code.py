import importlib

LEVEL = 11


def solution():
    module = importlib.import_module(f"student_solutions.level_{LEVEL}")
    student_solution = getattr(module, "solution", None)
    if not callable(student_solution):
        raise AttributeError(f"student_solutions.level_{LEVEL} must define solution()")
    return student_solution()
