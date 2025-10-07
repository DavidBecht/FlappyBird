from flappybird.game import bird
from flappybird.globals import globals

LEVEL = 10
def solution():
    pass
    # Füge hier deine Lösung ein!
    # print("Hi, David!")
    print(f"Alive: {bird.time_alive:.2f}")

    if bird.position_y > 450:
        bird.jump()