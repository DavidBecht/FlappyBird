<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 11: Sensoren**

Schreibe ein Programm, das den FlappyBird stoppt, bevor er gegen das Hindernis fliegt.
Benutze dazu den Sensor `bird.sensor_distances["right"]`, um den Abstand zum Hindernis zu messen.
Wenn der Abstand kleiner als 100 Pixel ist, soll der Vogel stoppen (`bird.stop()`) und `stopped` ausgegeben werden.

Füge deine Lösung in das File `student_code.py` ein!

```python
from flappybird.game import bird
LEVEL = 11

def solution():
    # Füge hier deine Lösung ein!
```

:::hint
Der Vogel hat Sensoren, die den Abstand zu Hindernissen messen können.
Du kannst auf die Sensoren zugreifen mit:
```python
dist_right = bird.sensor_distances["right"]
```
Andere Richtungen sind "up", "down", "left".

Um den Vogel zu stoppen, benutze:
```python
bird.stop()
```
:::

![level 11 solution](assets/level_11_solution.png)

:::solution
```python
from flappybird.game import bird
LEVEL = 11

def solution():
    if bird.sensor_distances["right"] < 100:
        bird.stop()
        print("stopped")
```
:::
