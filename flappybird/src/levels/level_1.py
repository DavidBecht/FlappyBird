from flappybird.src.levels.level_base import LevelBase

class Level1(LevelBase):
    def validate(self, text: str) -> bool:
        return text.lower().startswith("hi, ") and text.endswith("!") and len(text) > 6
