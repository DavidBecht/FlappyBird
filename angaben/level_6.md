<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 6: Erste Entscheidungen**

Schreibe ein Programm, das abhängig von der Y-Position des Vogels ausgibt:

- `Zu tief`, wenn der Vogel **unterhalb** der Bildschirmmitte ist
- `Zu hoch`, wenn der Vogel **oberhalb oder auf** der Bildschirmmitte ist

Füge deine Lösung in das File `student_code.py` ein!

```python
from flappybird.game import bird
from flappybird.globals import globals
LEVEL = 6

def solution():
    # Füge hier deine Lösung ein!
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
