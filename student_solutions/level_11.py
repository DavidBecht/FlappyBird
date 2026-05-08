from flappybird.game import bird

LEVEL = 11


def solution():
    right_distance = bird.sensor_distances["right"]
    if right_distance < 100:
        bird.stop()
        print("stopped")
