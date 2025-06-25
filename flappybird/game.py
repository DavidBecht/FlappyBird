from flappybird.src.game.game import FlappyBird
from flappybird.src.player.player import Player

class _LazyBird:
    def __getattr__(self, item):
        from flappybird.src.levels.level_manager_instance import level_manager
        return getattr(level_manager._flappy_bird._player, item)

bird: Player = _LazyBird()

class _LazyGame:
    def __getattr__(self, item):
        from flappybird.src.levels.level_manager_instance import level_manager
        return getattr(level_manager._flappy_bird, item)

game: FlappyBird = _LazyGame()
