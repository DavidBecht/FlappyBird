<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 6: Erste Entscheidungen**

Schreibe ein Programm, das abhängig von der Y-Position des Vogels ausgibt:

- `Zu tief`, wenn der Vogel **unterhalb** der Bildschirmmitte ist
- `Zu hoch`, wenn der Vogel **oberhalb oder auf** der Bildschirmmitte ist

Schreibe deine Lösung in die Datei `student_solutions/level_6.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!

```python
from flappybird.game import bird, start_level
from flappybird.globals import globals
LEVEL = 6

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

:::hint
Die Bildschirmmitte auf der Y-Achse ist:
```python
mitte = globals.SCREEN_HEIGHT / 2
```
:::

:::solution
```python
from flappybird.game import bird
from flappybird.globals import globals

LEVEL = 6

def solution():
    if bird.position_y > globals.SCREEN_HEIGHT / 2:
        print("Zu tief")
    else:
        print("Zu hoch")
```
:::
