from flappybird.src.game.game import FlappyBird
from flappybird.src.player.player import Player

def _running_level_manager():
    from flappybird.src.levels.level_manager_instance import level_manager
    if level_manager is None:
        raise RuntimeError("Das Spiel läuft noch nicht. Starte deine level_X.py-Datei mit ▶.")
    return level_manager

class _LazyBird:
    def __getattr__(self, item):
        return getattr(_running_level_manager()._flappy_bird._player, item)

bird: Player = _LazyBird()

class _LazyGame:
    def __getattr__(self, item):
        return getattr(_running_level_manager()._flappy_bird, item)

game: FlappyBird = _LazyGame()


def start_level(level, solution):
    """Startet das Spiel mit dem Level und der solution() aus einer level_X.py."""
    import os
    import re
    import flappybird.src.levels.level_manager_instance as lmi
    from flappybird.src.levels.level_manager import LevelManager

    # Kopierte Datei, LEVEL vergessen anzupassen? Lieber gleich sagen.
    file_name = os.path.basename(solution.__code__.co_filename)
    match = re.fullmatch(r"level_(\d+)\.py", file_name)
    if match and int(match.group(1)) != level:
        raise ValueError(f"In {file_name} steht LEVEL = {level}. Ändere es auf LEVEL = {match.group(1)}.")

    lmi.level_manager = LevelManager(level, solution)
    lmi.level_manager.load_level()
    lmi.level_manager.start_game()
