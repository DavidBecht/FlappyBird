<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 7: Schleifen-Einstieg**

Schreibe ein Programm, das mithilfe einer Schleife die Zahlen **1**, **2** und **3** ausgibt – jede Zahl in einer eigenen Zeile.

Erwartete Ausgabe:
```
1
2
3
```

Schreibe deine Lösung in die Datei `student_solutions/level_7.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!

```python
from flappybird.game import start_level

LEVEL = 7

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

:::hint
Mit `range(1, 4)` kannst du über die Zahlen 1 bis 3 laufen:
```python
for i in range(1, 4):
    print(i)
```
:::

:::solution
```python
LEVEL = 7

def solution():
    for i in range(1, 4):
        print(i)
```
:::
