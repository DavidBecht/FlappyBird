from flappybird.game import bird, start_level

LEVEL = 11


def solution():
    right_distance = bird.sensor_distances["right"]

    print(right_distance)
    if right_distance < 100:
        bird.stop()
        print("stopped")


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
