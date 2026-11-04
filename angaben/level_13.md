<style>
.solution {
  display: none;
}
</style>

# **FlappyBird Level 13: for-Schleife**

Schreibe ein Programm, das mithilfe einer **for-Schleife** und der Funktion `range()` die Summe aller Zahlen von **1 bis 100** berechnet und folgendes ausgibt:

```
Die Summe von 1 bis 100 ist 5050
```

Schreibe deine Lösung in die Datei `student_solutions/level_13.py` (gibt es sie noch nicht, lege sie an) und starte sie mit ▶!

```python
from flappybird.game import start_level

LEVEL = 13

def solution():
    # Füge hier deine Lösung ein!


# Startet das Spiel mit diesem Level. Nicht ändern!
if __name__ == "__main__":
    start_level(LEVEL, solution)
```

:::hint
Mit `range(start, stop)` erzeugt Python eine Folge von ganzen Zahlen von `start` bis **ausschließlich** `stop`.

```python
for zahl in range(1, 6):
    print(zahl)
```
> **Output:**
> ```
> 1
> 2
> 3
> 4
> 5
> ```

Um eine Summe aufzubauen, kannst du eine **Akkumulatorvariable** verwenden:
```python
summe = 0
for zahl in range(1, 4):
    summe += zahl   # gleichbedeutend mit: summe = summe + zahl
print(summe)        # 6
```
:::

:::solution
```python
LEVEL = 13

def solution():
    # Füge hier deine Lösung ein!
    summe = 0
    for zahl in range(1, 101):
        summe += zahl
    print(f"Die Summe von 1 bis 100 ist {summe}")
```
:::
