<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 14: Autopilot**

Schreibe einen **Autopiloten**, der den FlappyBird mithilfe der Sensoren automatisch durch die Röhren steuert und dabei **mindestens 20 Sekunden** überlebt.

Der Vogel darf **keine Röhre berühren** und darf den **Bildschirmrand nicht verlassen**.

Schreibe deine Lösung in die Datei `student_solutions/level_14.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!

```python
from flappybird.game import bird, start_level
from flappybird.globals import globals
LEVEL = 14

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

:::hint
Nutze die **Sensoren** des Vogels, um Abstände zu Hindernissen zu messen:

```python
dist_unten = bird.sensor_distances["down"]
dist_oben  = bird.sensor_distances["up"]
```

Fliegt der Vogel zu tief, springe nach oben:
```python
if dist_unten < 150:
    bird.jump()
```

Du kannst auch die **Y-Position** des Vogels mit der Bildschirmmitte vergleichen:
```python
from flappybird.globals import globals
mitte = globals.SCREEN_HEIGHT / 2
if bird.position_y > mitte:
    bird.jump()
```
:::

:::solution
```python
from flappybird.game import bird
from flappybird.globals import globals

LEVEL = 14

def solution():
    # Füge hier deine Lösung ein!
    if bird.sensor_distances["down"] < bird.sensor_distances["up"]:
        bird.jump()
```
:::
